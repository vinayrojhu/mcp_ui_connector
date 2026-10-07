# API contract

All endpoints currently run without authentication in local development. Do not expose them publicly.

- `GET /health` → `{ "status": "ok" }`
- `POST /api/plan` body `{ "request": "...", "application_id": "mock-fund-portal" }` → typed task plan.
- `POST /api/connectors/propose` same body → `{ "plan": ..., "connector": ... }`; policy failures return 422.
- `GET /api/connectors` → connector registry rows.
- `POST /api/executions` body connector JSON → execution id, status, event array, result.
- `GET /api/executions` → execution history.
- `GET /api/executions/{id}/events` → Server-Sent Events with `data: {"type":"step.completed",...}` and a `done` event.
- `POST /api/approvals/{execution_id}` body `{ "approved": true }` → records a one-execution decision. High-risk connectors pause in `pending_approval`; approval resumes the simulated executor, while rejection ends the run.

Errors use FastAPI's `{ "detail": "..." }` form. The production error envelope and correlation id middleware are not implemented yet.
