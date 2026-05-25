# Sequence: PR Merge Happy Path

Code development, SonarQube quality gate, and peer review through merge.

## Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant IDE as IDE + SonarLint
    participant GenAI as Copilot / Cursor
    participant Git as Git / PR
    participant CI as ADO Pipeline
    participant Sonar as SonarQube
    participant Rev as Peer Reviewer
    participant ADO as ADO Work Items

    Dev->>ADO: Pick work item
    Dev->>Git: Create branch
    Dev->>GenAI: Assist implementation
    GenAI-->>Dev: Suggested code and tests
    Dev->>IDE: Edit + local analysis
    IDE-->>Dev: Issues and fixes
    Dev->>Dev: Run unit tests locally
    Dev->>Git: Push + create PR
    Dev->>ADO: Link PR to work item

    Git->>CI: Webhook PR build
    CI->>CI: Build + unit tests
    CI->>Sonar: Upload analysis
    Sonar-->>CI: Quality Gate result

    alt Quality Gate failed
        CI-->>Git: Check failed
        Dev->>Git: Push fixes
    else Quality Gate passed
        CI-->>Git: Check passed
        Git->>Rev: Review requested
        Rev->>Git: Review comments
        alt Changes requested
            Dev->>Git: Address feedback + push
        else Approved
            Rev->>Git: Approve PR
            Dev->>Git: Merge
            Git->>CI: Main branch build
        end
    end
```

## Preconditions

- Branch policy requires PR to `main`
- SonarQube project bound to repository
- CI service connection and Sonar token configured

## Postconditions

- `main` build succeeds
- SonarQube analysis on `main` updated
- Work item can move to Done per team rules

## Failure handling

| Failure | Action |
|---------|--------|
| Unit test fail | Developer fixes locally; re-push |
| Quality gate fail | Fix code or tests; check coverage on new code |
| Review rejected | Address comments; no merge until re-approval |

## KPI linkage

- **Merge-ready after review:** first approval without major rework
- **Merge <1 business day:** timestamp PR created → merged (business hours)

## Related

- [../workflow/sub-workflows.md](../workflow/sub-workflows.md#1-code-development-code-review-code-quality)
- [robot-e2e.md](robot-e2e.md)
