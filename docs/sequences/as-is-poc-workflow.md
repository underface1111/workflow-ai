# Sequence: POC As-Is (workflow-ai hiện tại)

Luồng **đang triển khai** trên GitHub — human-in-the-loop + CI guardrails. Không có AI Orchestrator tự động.

## Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant IDE as Cursor + SonarLint
    participant Git as GitHub PR
    participant CI as GitHub Actions
    participant Sonar as SonarCloud
    participant Robot as Robot E2E
    participant Rev as Peer Reviewer

    Dev->>IDE: Code + tests (assisted by Cursor rules)
    IDE-->>Dev: SonarLint feedback
    Dev->>Dev: npm test local
    Dev->>Git: Push branch + open PR

    Git->>CI: pull_request / push
    CI->>CI: npm ci + jest coverage
    CI->>Sonar: Scanner upload
    Sonar-->>CI: Quality Gate

    alt QG fail
        CI-->>Dev: Failed check
        Dev->>Git: Fix + push
    else QG pass
        CI->>Robot: Start API + @critical suites
        Robot-->>CI: output.xml
        alt Robot fail
            CI-->>Dev: Failed check
        else Robot pass
            CI-->>Git: Checks green
            Git->>Rev: Review requested
            Rev->>Git: Approve
            Dev->>Git: Merge to main
            Git->>CI: CI on main
        end
    end
```

## Mapping repo

| Bước | Artifact |
|------|----------|
| Local test | `npm test`, `npm run test:e2e` |
| CI unit + Sonar | `.github/workflows/ci.yml` job `build-test-sonar` |
| Robot | job `e2e-robot` |
| Sonar config | `sonar-project.properties` |
| IDE | `.vscode/settings.json`, `docs/dev/sonarlint-cursor.md` |

## Khác To-Be

- Không có Orchestrator, AI Code/Test Agent, auto PR, self-heal.
- Xem [ai-orchestrator-to-be.md](ai-orchestrator-to-be.md).

## Related

- [pr-merge-happy-path.md](pr-merge-happy-path.md)
- [../plan/as-is-vs-to-be.md](../plan/as-is-vs-to-be.md)
