# Contributing — workflow-ai POC

Aligned with the BankCo **Development & Test** workflow (peer review, SonarQube, Robot `@critical`, GenAI guardrails).

## Prerequisites

- Node.js 20+
- npm
- **SonarLint** in Cursor — see [docs/dev/sonarlint-cursor.md](docs/dev/sonarlint-cursor.md)
- (E2E) Python 3.10+ and Robot Framework — see `tests/e2e-robot/README.md`
- (Load) k6 — see `perf/k6/README.md`

## Local development

```bash
npm ci
npm run dev          # API on :3000
npm test             # unit + coverage
```

Demo credentials: `demo@bankco.local` / `demo123`

## AI-generated unit tests (Bước B)

- **Đang học:** `npm run ai:test-gen` (template) vì chưa có API key; sau này `npm run ai:test-gen:llm` (cùng validate).
- Validate: `npm run ai:test-validate` — CI: validate + Jest (B4), chưa gọi LLM trên GitHub.
- **Review diff before commit** (B5).

## AI Code Agent (Bước C)

- Requirements → patch: `npm run ai:code-gen:learn-003` hoặc `npm run ai:code-slice`
- Validate: `npm run ai:code-validate`
- **Luôn dùng feature branch + PR** — không push thẳng `main` (C4)
- Manual CI: Actions → **AI Pipeline** → `learn-003` (template, không commit trên runner)

See [tools/ai-code-gen/README.md](tools/ai-code-gen/README.md).

## AI Robot E2E (Bước D)

- Generate: `npm run ai:robot-gen:learn-004` → `tests/e2e-robot/suites/generated/*.robot`
- Tags: **`generated`** only — không gắn tag `critical` lên suite AI
- CI: `critical` (stable) rồi `generated` (riêng output `robot-results-generated/`)
- **Review diff `.robot` trước merge** (D3)

See [tools/ai-robot-gen/README.md](tools/ai-robot-gen/README.md).

## Release pipeline (Bước E)

- `npm run ai:release-pipeline -- --branch <feature-branch> --ticket learn-005`
- Cần `GITHUB_TOKEN` để tạo PR; `MENTOR_GITHUB_LOGIN` cho @mention
- **Không auto-merge** — human review + CI required checks
- Actions: **Release Pipeline** (`workflow_dispatch`)

See [docs/dev/release-pipeline.md](docs/dev/release-pipeline.md).

## Pull request checklist

- [ ] ADO work item linked in PR description
- [ ] Unit tests added/updated; `npm test` passes
- [ ] SonarLint clean on touched files
- [ ] SonarQube Quality Gate passes on PR
- [ ] Peer review approval (target: merge-ready on first round)
- [ ] If critical paths changed: Robot `--include critical` passes
- [ ] No secrets, API keys, or PII in code or GenAI prompts

## GenAI usage

- Use Copilot/Cursor with squad rules in `.cursor/rules/`
- Human review required for all AI-generated logic (ADR-05)
- Do not disable Sonar rules to pass the gate

## Code standards

- Express handlers stay thin; logic in `src/` modules covered by unit tests
- New API routes require unit tests and, if user-facing journey, Robot steel-thread update
- Coverage threshold in `package.json` (minimum 50% lines — raise via Sonar new-code gate)

## Review labels

- `merge-ready` — QG green, tests pass, approval received, E2E (if applicable) pass
