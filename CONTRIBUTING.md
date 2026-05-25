# Contributing — workflow-ai POC

Aligned with the BankCo **Development & Test** workflow (peer review, SonarQube, Robot `@critical`, GenAI guardrails).

## Prerequisites

- Node.js 20+
- npm
- (E2E) Python 3.10+ and Robot Framework — see `tests/e2e-robot/README.md`
- (Load) k6 — see `perf/k6/README.md`

## Local development

```bash
npm ci
npm run dev          # API on :3000
npm test             # unit + coverage
```

Demo credentials: `demo@bankco.local` / `demo123`

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
