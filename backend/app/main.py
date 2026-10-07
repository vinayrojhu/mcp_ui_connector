import asyncio
import json
from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import engine, get_db
from app.models.entities import AuditEvent, Base, Connector, Execution
from app.schemas import ApprovalRequest, ConnectorDefinition, TaskRequest
from app.services.orchestrator import build_connector, event, execute_mock, plan_task
from app.services.policy import PolicyError, requires_approval, validate_connector

app = FastAPI(title="Adaptive UI Connector Platform", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/plan")
async def create_plan(task: TaskRequest):
    return (await plan_task(task)).model_dump()


@app.post("/api/connectors/propose")
async def propose(task: TaskRequest):
    plan = await plan_task(task)
    connector = await build_connector(task, plan)
    try:
        validate_connector(connector)
    except PolicyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"plan": plan.model_dump(), "connector": connector.model_dump()}


@app.get("/api/connectors")
async def list_connectors(db: AsyncSession = Depends(get_db)):
    rows = (await db.scalars(select(Connector).order_by(Connector.created_at.desc()))).all()
    return [{"id": r.id, "name": r.name, "application_id": r.application_id, "environment": r.environment,
             "version": r.version, "success_count": r.success_count, "status": r.status} for r in rows]


@app.post("/api/executions")
async def create_execution(connector: ConnectorDefinition, db: AsyncSession = Depends(get_db)):
    try:
        validate_connector(connector)
    except PolicyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    execution_id = str(uuid4())
    approval_needed = any(requires_approval(step) for step in connector.steps)
    execution = Execution(id=execution_id, request=connector.name, definition=connector.model_dump(),
                          status="pending_approval" if approval_needed else "completed")
    if approval_needed:
        events = [event("approval.required", "Approval is required before this action", scope="single_execution")]
        result = None
    else:
        events, result = await execute_mock(connector)
    execution.events, execution.result = events, result
    db.add(execution)
    if not approval_needed:
        db.add(Connector(name=connector.name, application_id=connector.application_id,
                         environment=connector.environment, definition=connector.model_dump(), success_count=1))
    db.add(AuditEvent(execution_id=execution_id,
                      event_type="approval.required" if approval_needed else "execution.completed",
                      detail={"validated": True, "approval_required": approval_needed}))
    await db.commit()
    return {"id": execution_id, "status": execution.status, "events": events, "result": result}


@app.get("/api/executions")
async def list_executions(db: AsyncSession = Depends(get_db)):
    rows = (await db.scalars(select(Execution).order_by(Execution.created_at.desc()))).all()
    return [{"id": r.id, "status": r.status, "request": r.request, "created_at": r.created_at.isoformat()} for r in rows]


@app.get("/api/executions/{execution_id}/events")
async def stream_events(execution_id: str, db: AsyncSession = Depends(get_db)):
    execution = await db.get(Execution, execution_id)
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    async def feed():
        for item in execution.events:
            yield f"data: {json.dumps(item)}\n\n"
            await asyncio.sleep(0.05)
        yield "event: done\ndata: {}\n\n"
    return StreamingResponse(feed(), media_type="text/event-stream")


@app.post("/api/approvals/{execution_id}")
async def approval(execution_id: str, decision: ApprovalRequest, db: AsyncSession = Depends(get_db)):
    execution = await db.get(Execution, execution_id)
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    if execution.status != "pending_approval":
        raise HTTPException(status_code=409, detail="Execution is not waiting for approval")
    if decision.approved:
        connector = ConnectorDefinition.model_validate(execution.definition)
        events, result = await execute_mock(connector)
        execution.status, execution.events, execution.result = "completed", events, result
        db.add(Connector(name=connector.name, application_id=connector.application_id,
                         environment=connector.environment, definition=connector.model_dump(), success_count=1))
        kind = "approval.approved"
    else:
        execution.status = "rejected"
        execution.events = [*execution.events, event("approval.rejected", "Execution was rejected")]
        kind = "approval.rejected"
    db.add(AuditEvent(execution_id=execution_id, event_type=kind,
                      detail={"scope": "single_execution", "decision": decision.approved}))
    await db.commit()
    return {"execution_id": execution_id, "decision": "approved" if decision.approved else "rejected",
            "status": execution.status, "scope": "single execution"}
