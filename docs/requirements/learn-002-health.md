# Health endpoint requirements (LEARN-002)

Đầu vào cho **Bước B+** — vòng 2: template → validate → PR.

---

## Metadata

| Field | Value |
|-------|--------|
| Ticket ID | LEARN-002 |
| Title | Unit tests for GET /health |
| Author | @developer |
| Target branch | `feature/learn-002-health` |

---

## User story

As an operator, I want a public health endpoint so that load balancers and monitors can verify the service is up without credentials.

---

## Acceptance criteria

1. `GET /health` returns HTTP 200.
2. Body JSON: `{ "status": "ok", "service": "workflow-ai-poc" }`.
3. No authentication required.
4. Generated unit test in `tests/unit/generated/` covers the happy path.
5. Existing steel thread and LEARN-001 tests still pass.

---

## Technical notes

- Stack: Node.js Express, CommonJS.
- Endpoint already exists in `src/app.js` — this ticket adds **generated test only**.
- Import app from `../../../src/app` in generated files.

---

## Out of scope

- Changing `/health` response shape
- Robot suite changes
- k6 script changes

---

## For AI Test Agent

```json
{
  "ticket_id": "LEARN-002",
  "tasks": ["unit_test"],
  "output_format": "json_schema_v1",
  "constraints": ["no_secrets", "preserve_steel_thread"]
}
```
