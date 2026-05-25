# AI Test Agent (Evolution roadmap — Bước B)

Sinh **Jest unit tests** từ `docs/requirements/*.md`, validate bằng **Pydantic** (`schemas.py`).

**Hiện tại (chưa có API key):** dùng `--template` + `validate.py`.  
**Khi có key:** thêm bước LLM (Anthropic/OpenAI) — cùng schema, cùng validate.

## Setup

```bash
# Đủ cho template + validate (không cần key)
python -m pip install -r tools/ai-test-gen/requirements-validate.txt

# Thêm khi dùng LLM
python -m pip install -r tools/ai-test-gen/requirements.txt
```

`.env` (repo root, **không commit**):

```env
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-haiku-4-5
```

## Luồng đang dùng (tạm thời không có API key)

```bash
npm run ai:test-gen           # template
npm run ai:test-validate      # validate + npm test
```

CI cũng chỉ **validate + Jest** — không gọi LLM vì chưa cấu hình secret trên GitHub (có thể bật sau).

## Khi đã có API key — LLM

```bash
npm run ai:test-gen:llm
# hoặc
python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md --provider anthropic
npm run ai:test-validate
```

| Provider | Env |
|----------|-----|
| Anthropic (mặc định) | `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` |
| OpenAI | `OPENAI_API_KEY`, `--provider openai` |

## Bước B4 — Validate (CI + local)

- Header `AUTO-GENERATED`, `REVIEW REQUIRED`
- Pydantic: Jest + supertest + import `src/app`
- CI: `validate.py --skip-npm` → `npm run test:ci`

## Review policy (B5)

- Review diff trước merge `tests/unit/generated/*.test.js`

## Contract

`schemas.py` — `GeneratedUnitTest` / `json_schema_v1`
