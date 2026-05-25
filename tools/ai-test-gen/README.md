# AI Test Agent (Evolution roadmap — Bước B)

Generate **Jest unit tests** from `docs/requirements/*.md` with **Pydantic** validation (`schemas.py`).

## Setup

```bash
python -m pip install -r tools/ai-test-gen/requirements.txt
```

Optional in `.env` (local only, never commit):

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
# OPENAI_BASE_URL=https://...  # optional compatible API
```

## Usage

### 1. Template mode (no API) — `LEARN-001` / example-feature

```bash
python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md --template
```

Writes `tests/unit/generated/learn-001-root.test.js`.

### 2. LLM mode

```bash
python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md
```

### 3. Verify

```bash
npm test
```

## Review policy (B5)

- Files under `tests/unit/generated/` are **drafts** until a human reviews.
- Header comment: `REVIEW REQUIRED before merge`.
- Do not merge generated tests without reading diff.

## Contract

JSON shape validated by `AgentResponse` / `GeneratedUnitTest` in `schemas.py` — aligns with `example-feature.md` `json_schema_v1`.

## Next (roadmap)

- B4: optional CI job `workflow_dispatch` to run generator + `npm test`
- C: AI Code Agent for `src/` changes
