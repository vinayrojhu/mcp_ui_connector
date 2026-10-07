# Connector schema

The canonical JSON Schema is [connector.schema.json](../shared_schemas/connector.schema.json). Pydantic models live in `backend/app/schemas.py`; matching TypeScript types are in `frontend/lib/api.ts`.

Top-level fields: `schema_version`, `name`, `application_id`, `environment`, `inputs`, `preconditions`, `steps`, and `expected_result`. Actions are limited to click, fill, press, navigate, download, and wait. Targets use accessible role/name, label, exact text, or configured test id. Actions include a risk and one-time approval requirement marker. Policy independently blocks domains and unregistered applications.

Example:

```json
{"schema_version":"1.0","name":"Search fund","application_id":"mock-fund-portal","environment":"browser","inputs":["query"],"preconditions":[],"steps":[{"type":"fill","target":{"role":"textbox","name":"Search"},"value":"{{query}}","risk":"low","approval_required":false}],"expected_result":"Matching fund is visible"}
```
