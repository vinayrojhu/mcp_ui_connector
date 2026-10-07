# Adaptive UI Connector Platform

An MVP scaffold for describing UI tasks, proposing a validated declarative connector, reviewing it, and recording local execution events. LLM calls have a provider boundary; mock mode is the default. The included API executor is simulated. The Playwright worker contains a local action adapter, but it is not wired to a persistent authenticated browser session yet. The Windows worker reports and inspects UI Automation controls when run in an interactive Windows session.

## Architecture

Next.js submits a task to FastAPI. The planner returns a typed plan, the generator returns a connector conforming to the shared schema, and the policy layer checks the application, action types, step cap, and navigation domain. Successful mock executions are persisted with connector and audit records. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Prerequisites and setup

- Python 3.12+
- Node.js 20+
- Docker Compose (optional, for PostgreSQL)
- Windows 10/11 and an interactive user session for desktop inspection

Copy `.env.example` to `.env` and replace secrets before using anything beyond local mock mode. The backend defaults to local SQLite so it can start without Docker; Compose configures PostgreSQL.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .\backend[dev]
cd backend
uvicorn app.main:app --reload
```

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. API docs are at http://localhost:8000/docs. To use Compose, copy `.env.example` to `.env`, then run `docker compose up --build`; the mock fund portal is at http://localhost:8080.

## Workers and tests

Install the browser extra with `pip install -e .\backend[workers]`, install Chromium using `python -m playwright install chromium`, and use `browser_worker/worker.py` from a locally managed browser session. Run `python desktop_worker/worker.py` only from a Windows interactive user session after installing worker dependencies. Desktop input, screenshot capture, OCR, and approval-bound actions are not connected to the API executor.

Run policy tests with `cd backend; python -m pytest ../tests`. The sample portal can also be served using `python -m http.server 8080 --directory mock_apps`.

## Supported functionality

- Task and connector proposal UI
- Typed plan and connector models
- Application and navigation allowlists
- Simulated execution, history, SSE event stream, connector storage, and audit events
- Local Playwright accessible locator adapter
- Windows UI Automation inspection adapter

## Security and MVP limits

LLM output is treated as untrusted and validated before use. Connector actions are enumerated; arbitrary source code and shell commands are not part of the schema. Credentials and browser values are not included in inspection metadata. Authentication, encrypted provider-key storage, approval expiration, connector repair/versioning, and production-grade worker authentication need implementation before exposing this system to users. High-risk work pauses for one-execution approval in mock mode. Do not connect sensitive accounts to this MVP.
