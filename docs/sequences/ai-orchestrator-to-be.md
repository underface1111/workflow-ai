# Sequence: AI Orchestrator (To-Be)

Luồng **mục tiêu** — ticket/requirements → dual AI → guardrails → auto PR hoặc self-heal. **Chưa triển khai** trong repo.

## Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / PM
    participant Orch as Workflow Orchestrator
    participant AICode as AI Code Agent
    participant AITest as AI Test Agent
    participant Guard as Guardrails
    participant Sonar as SonarQube
    participant Test as Test Runner
    participant Repo as GitHub

    Dev->>Orch: 1. Requirements / Jira ticket
    activate Orch

    Orch->>AICode: 2. Generate feature code
    activate AICode
    AICode-->>Orch: 3. Code files (JSON contract)
    deactivate AICode

    Orch->>AITest: 4. Generate tests from code
    activate AITest
    AITest-->>Orch: 5. Jest / Robot scripts
    deactivate AITest

    Orch->>Guard: 6. Submit code + tests
    activate Guard
    Guard->>Sonar: Static scan
    Guard->>Test: Run tests + coverage

    alt Fail Sonar or coverage below 50%
        Guard-->>Orch: 7a. Structured error log
        Orch->>AICode: 8a. Self-heal request (max 3 loops)
        Note over Orch,AICode: Optional: also AITest
    else Pass all gates
        Guard-->>Orch: 7b. OK
        deactivate Guard
        Orch->>Repo: 8b. Push branch + create PR
        activate Repo
        Repo-->>Dev: 9. Notify mentor for review
        deactivate Repo
    end

    deactivate Orch
```

## Guardrails detail (To-Be)

| Check | Tool (POC tương đương) |
|-------|-------------------------|
| Static | SonarCloud (`sonar-project.properties`) |
| Unit + coverage | Jest (`npm run test:ci`) |
| E2E critical | Robot (`tests/e2e-robot/`) |
| Load (optional) | k6 — not in PR gate |

## Human-in-the-loop (bắt buộc)

- Auto PR **không** auto-merge (align ADR-05, BankCo ~80% merge-ready after review).
- Mentor approves on GitHub UI.

## Implementation status

| Step | Status in repo |
|------|----------------|
| 1–5 AI pipeline | Not implemented |
| 6 Guardrails | Implemented (CI) |
| 8b Auto PR | Not implemented |
| 8a Self-heal | Not implemented |

Roadmap: [../plan/evolution-roadmap.md](../plan/evolution-roadmap.md).

## Related

- [as-is-poc-workflow.md](as-is-poc-workflow.md)
- [../plan/target-ai-orchestrator.md](../plan/target-ai-orchestrator.md)
