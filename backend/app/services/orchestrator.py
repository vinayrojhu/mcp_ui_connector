from datetime import datetime, timezone
from app.schemas import ConnectorDefinition, Plan, TaskRequest
from app.services.llm import provider


def event(kind: str, message: str, **extra):
    return {"type": kind, "message": message, "timestamp": datetime.now(timezone.utc).isoformat(), **extra}


async def plan_task(task: TaskRequest) -> Plan:
    return await provider.plan(task)


async def build_connector(task: TaskRequest, plan: Plan) -> ConnectorDefinition:
    return await provider.generate(task, plan)


async def execute_mock(connector: ConnectorDefinition):
    """The MVP worker boundary returns simulated observations; no device is controlled here."""
    result_events = [event("execution.started", "Execution started")]
    for index, step in enumerate(connector.steps, start=1):
        result_events.append(event("step.completed", f"Completed step {index}", step=index))
    result_events.append(event("execution.completed", "Observed expected result", outcome="success"))
    return result_events, {"valid": True, "summary": connector.expected_result}
