# Release pipeline (LEARN-005) — Bước E

Đóng vòng: test → self-heal → mở PR → tag mentor. **Không auto-merge.**

---

## Metadata

| Field | Value |
|-------|--------|
| Ticket ID | LEARN-005 |
| Title | Orchestrated PR with self-heal guardrails |
| Target branch | `feature/learn-005-*` (pushed to origin) |

---

## Acceptance criteria

1. `npm test` pass (sau tối đa 3 self-heal template).
2. PR opened against `main` (hoặc dùng PR đang mở cho cùng branch).
3. Comment trên PR tag `@mentor` (login từ `MENTOR_GITHUB_LOGIN`).
4. Metrics JSON trong `orchestrator/out/`.
5. Human merge sau CI + approval.

---

## Env

| Variable | Mục đích |
|----------|----------|
| `GITHUB_TOKEN` | Tạo PR + comment (Actions: `secrets.GITHUB_TOKEN`) |
| `MENTOR_GITHUB_LOGIN` | User được @mention (default: `mentor`) |

---

## Self-heal templates (POC)

| Signal | Fix |
|--------|-----|
| JUnit thiếu `version` / health | `ai-code-gen` LEARN-003 |
| Robot / learn-004 | `ai-robot-gen` LEARN-004 |

Optional: copy `orchestrator/in/sonar-hints.json.example` → `sonar-hints.json`.
