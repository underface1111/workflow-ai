# Health version field (LEARN-003)

Đầu vào cho **Bước C** — AI Code Agent (patch `src/`).

---

## Metadata

| Field | Value |
|-------|--------|
| Ticket ID | LEARN-003 |
| Title | Add version field to GET /health |
| Author | @developer |
| Target branch | `feature/learn-003-health-version` |

---

## User story

As an operator, I want the health endpoint to expose an API version so deploy pipelines can verify the running build.

---

## Acceptance criteria

1. `GET /health` returns HTTP 200.
2. Body includes `"version": "0.2.0"` in addition to `status` and `service`.
3. `tests/unit/app.test.js` asserts the version field.
4. Generated test `learn-002-health.test.js` updated to expect version (if present).
5. Steel thread and existing tests still pass.

---

## Technical notes

- Stack: Node.js Express, CommonJS.
- Only touch: `src/app.js`, `tests/unit/app.test.js`, `tests/unit/generated/learn-002-health.test.js`.
- Do not change auth or cart/checkout behavior.

---

## Out of scope

- OpenAPI / Swagger
- Environment-based version from `process.env` (use literal `0.2.0` for POC)

---

## For AI Code Agent

```json
{
  "ticket_id": "LEARN-003",
  "tasks": ["code"],
  "output_format": "json_schema_v1",
  "constraints": ["no_secrets", "preserve_steel_thread", "allow_paths": ["src/", "tests/unit/"]]
}
```
