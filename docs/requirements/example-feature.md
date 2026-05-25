# Example feature requirements (input template)

Dùng làm **đầu vào** cho Giai đoạn 2 (AI Orchestrator). Dev hoặc PM điền trước khi chạy pipeline.

---

## Metadata

| Field | Value |
|-------|--------|
| Ticket ID | LEARN-001 |
| Title | Add GET / root info endpoint |
| Author | @developer |
| Target branch | `feature/learn-001-root` |

---

## User story

As an API consumer, I want a root endpoint so that I can confirm the service identity without calling authenticated routes.

---

## Acceptance criteria

1. `GET /` returns HTTP 200.
2. Body JSON: `{ "message": "workflow-ai-poc", "docs": "/health" }`.
3. No authentication required.
4. Unit test covers happy path and method not allowed (if applicable).
5. Existing steel thread tests still pass.

---

## Technical notes

- Stack: Node.js Express, CommonJS.
- Files likely touched: `src/app.js`, `tests/unit/app.test.js`.
- Do not change auth behavior on `/catalog`, `/cart`, `/checkout`.
- Coverage on new code must meet Sonar **new code** gate.

---

## Out of scope

- UI changes
- Database
- k6 load test updates (optional follow-up)

---

## Definition of done (POC / BankCo aligned)

- [ ] SonarLint clean on touched files
- [ ] `npm test` pass locally
- [ ] PR opened; CI green (unit, Sonar, Robot `@critical`)
- [ ] Peer review approval
- [ ] Merged to `main`

---

## For future AI Orchestrator

```json
{
  "ticket_id": "LEARN-001",
  "tasks": ["code", "unit_test"],
  "output_format": "json_schema_v1",
  "constraints": ["no_secrets", "preserve_steel_thread"]
}
```

Schema và agent: see [../plan/evolution-roadmap.md](../plan/evolution-roadmap.md) Bước B.
