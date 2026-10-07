# Development

Backend modules separate Pydantic schemas, persistence entities, mock provider, policy checks, and orchestration. Add an LLM provider by implementing the asynchronous `plan` and `generate` methods on the provider boundary; parse output through existing schemas and keep credentials server-side. Add browser actions only to the shared schema, policy validator, and worker adapter together. Desktop inspection requires Windows UI Automation in an interactive session.

Run the API and frontend using the commands in the root README. Database tables are created at startup for the MVP; Alembic migration scaffolding is not included. Policy tests live in `tests/`.
