# Security

## Trust boundaries

The LLM provider receives task text and structured inspection metadata only. Its output is untrusted JSON parsed into Pydantic models and checked against application, domain, action, and step-count policy. Workers execute a finite action vocabulary; the connector format cannot express Python, JavaScript, shell, SQL, arbitrary process launch, or direct approval.

## Current controls

- Application allowlist and URL hostname allowlist
- Finite action enum and strict Pydantic validation
- Accessible locator resolution with visibility, enabled-state, and uniqueness checks in the browser adapter
- Sensitive input values omitted from browser inspection metadata
- Database audit record for completed mock executions
- Mock execution is the default

## Deployment requirements

Replace development JWT and worker secrets, configure provider key storage, enable authentication and authorization, use TLS, restrict origins, set retention limits, and isolate worker processes before deployment. Screenshot redaction, encrypted secrets, approval enforcement around live worker calls, and identity verification are not implemented in this MVP. Do not use it to submit financial or other irreversible actions.
