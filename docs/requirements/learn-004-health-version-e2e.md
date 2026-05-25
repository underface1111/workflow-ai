# Health version E2E (LEARN-004)

Đầu vào **Bước D** — AI Robot E2E (generated suite).

---

## Metadata

| Field | Value |
|-------|--------|
| Ticket ID | LEARN-004 |
| Title | Robot E2E for GET /health version field |
| Author | @developer |
| Target branch | `feature/learn-004-robot-e2e` |

---

## User story

As QA, I want an API-level Robot test that asserts `/health` returns `version` so LEARN-003 is covered end-to-end without browser automation.

---

## Acceptance criteria

1. Suite lives under `tests/e2e-robot/suites/generated/`.
2. Tags: `generated`, `learn-004` (not `critical`).
3. Uses existing `api_keywords.robot` and `local.yaml`.
4. Asserts `status=ok` and `version=0.2.0` on `GET /health`.
5. Stable `critical` suite unchanged and still passes.

---

## Technical notes

- RequestsLibrary only (no Selenium).
- Do not duplicate full steel thread — health-only slice.

---

## For AI Robot Agent

```json
{
  "ticket_id": "LEARN-004",
  "tasks": ["robot_e2e"],
  "output_format": "json_schema_v1",
  "constraints": ["tag_generated_not_critical", "reuse_api_keywords"]
}
```
