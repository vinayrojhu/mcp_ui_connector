# Architecture

## Components and trust boundaries

The Next.js client talks to FastAPI. FastAPI owns planning, connector parsing, policy checks, persistence, event history, and audit records. LLM providers only return structured plans and connector JSON. Browser and desktop adapters run on the user's machine and accept declarative actions. The current API uses a simulated executor; the worker adapters are not remotely callable.

## Main workflow

1. `/api/connectors/propose` plans a task and builds a connector.
2. `validate_connector` rejects unregistered applications, excess steps, and disallowed navigation.
3. The UI displays plan and proposed connector for review.
4. `/api/executions` revalidates the connector, pauses high-risk work until a one-execution approval, writes execution and connector records, and emits stored execution events over SSE.
5. Audit events store completion metadata without task field values.

## Data model

- `Connector`: definition, app/environment identity, version, status, fingerprint, success count.
- `Execution`: task label, status, event list, validated result.
- `AuditEvent`: execution reference, event kind, structured safe detail.

SQLAlchemy creates tables for local development. Compose uses PostgreSQL; local default uses SQLite.

## Limitations

Persistent sessions, connector matching/repair, worker RPC, signed worker identity, application fingerprints, expiring approvals, and result observation against real applications remain outside the functioning vertical slice.
