# AI Test Agent (Evolution roadmap — Bước B)

Generate **Jest unit tests** from `docs/requirements/*.md` with **Pydantic** validation (`schemas.py`).

## Setup

```bash
python -m pip install -r tools/ai-test-gen/requirements.txt
```

Local `.env` (repo root, **never commit**):

```env
ANTHROPIC_API_KEY=sk-ant-...
# Default: cheapest Claude (Haiku 4.5). Alias: claude-haiku-4-5
ANTHROPIC_MODEL=claude-haiku-4-5
```

Optional OpenAI instead:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

The script loads `.env` automatically if present.

## Usage

### 1. Template mode (no API) — `LEARN-001` / example-feature

```bash
python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md --template
# or
npm run ai:test-gen
```

### 2. Claude / Anthropic (default when `ANTHROPIC_API_KEY` is set)

```bash
python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md
# explicit:
python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md --provider anthropic
# or
npm run ai:test-gen:llm
```

### 3. OpenAI

```bash
python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md --provider openai
```

### 4. Verify

```bash
npm test
```

## Provider selection

| Priority | Rule |
|----------|------|
| 1 | `--provider anthropic` or `openai` |
| 2 | If only `ANTHROPIC_API_KEY` → **anthropic** |
| 3 | If only `OPENAI_API_KEY` → **openai** |
| 4 | Default → **anthropic** (error if key missing) |

## Review policy (B5)

- Files under `tests/unit/generated/` are **drafts** until a human reviews.
- Header comment: `REVIEW REQUIRED before merge`.
- Do not merge generated tests without reading diff.

## Contract

JSON shape validated by `AgentResponse` / `GeneratedUnitTest` in `schemas.py` — aligns with `example-feature.md` `json_schema_v1`.

## Next (roadmap)

- B4: CI validate-only job (no API key on GitHub)
- C: AI Code Agent for `src/` changes
