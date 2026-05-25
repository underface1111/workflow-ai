# AI Code Agent (Bước C)

Sinh / áp patch **`src/`** và **`tests/unit/`** từ `docs/requirements/*.md`.

**POC:** `--template` cho LEARN-003 (không API). LLM sau khi có credit.

## Setup

```bash
python -m pip install -r tools/ai-code-gen/requirements.txt
```

## LEARN-003 — version on `/health`

```bash
npm run ai:code-gen:learn-003
npm run ai:code-validate
npm test
```

## Files

| File | Role |
|------|------|
| `schemas.py` | Pydantic — allowed paths `src/`, `tests/unit/` |
| `generate.py` | Template / (future) LLM |
| `validate.py` | Structural checks + `npm test` |

## Review (C + B5)

- Đọc diff `src/app.js` và tests trước khi commit.
- Không push thẳng `main` — feature branch + PR.

## Orchestrator

`orchestrator/run_code_slice.py` — wrapper gọi generate + validate (C2).
