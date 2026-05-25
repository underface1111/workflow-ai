# Macro Workflow — Development & Test

End-to-end flow from work item to release candidate, aligned with the BankCo GenAI SDLC slide.

## Full flowchart

```mermaid
flowchart TD
    START([Work Item in ADO]) --> DESIGN[Technical design / task breakdown]
    DESIGN --> BRANCH[Create feature branch]

    BRANCH --> DEVLOOP{Dev Loop}
    DEVLOOP --> CODE[Code + GenAI assist]
    CODE --> LINT[SonarLint local fix]
    LINT --> UNIT[Run unit tests locally]
    UNIT -->|fail| CODE
    UNIT -->|pass| PUSH[Push + Open PR]

    PUSH --> AUTO_CI[CI: Build + Unit + Sonar]
    AUTO_CI -->|QG fail| FIX[Fix issues]
    FIX --> CODE

    AUTO_CI -->|QG pass| PEER[Peer Review]
    PEER -->|changes requested| FIX
    PEER -->|approved| E2E_GATE{Critical path changed?}

    E2E_GATE -->|yes| ROBOT_CI[Deploy Test + Robot @critical]
    E2E_GATE -->|no| MERGE_READY
    ROBOT_CI -->|fail| FIX
    ROBOT_CI -->|pass| MERGE_READY[Mark merge-ready]

    MERGE_READY --> MERGE[Merge to main]
    MERGE --> MAIN_CI[CI on main]
    MAIN_CI --> NIGHTLY[Nightly: full E2E suite]

    NIGHTLY --> LOAD_SCHED{Release window?}
    LOAD_SCHED -->|yes| LOAD[Steel Thread load test]
    LOAD --> ARCH[Architecture validation review]
    ARCH --> DONE([Done / Release candidate])
```

## Stage summary

| Stage | Owner | Entry | Exit criteria |
|-------|-------|-------|---------------|
| Work item | PO / team | ADO backlog | Task ready with acceptance criteria |
| Dev loop | Developer | Branch created | Local unit pass; SonarLint acceptable |
| PR automation | CI | PR opened | Sonar quality gate pass |
| Peer review | Reviewer | QG green | Approval; ~80% target merge-ready first round |
| E2E (conditional) | CI + QA | Critical paths touched | `@critical` Robot pass |
| Merge | Developer | All gates green | On `main` |
| Nightly | CI | Merge to main | Full Robot suite reported |
| Load (scheduled) | Perf + Architect | Release window | Steel Thread SLA met; KPI updated |

## Gate model

```mermaid
flowchart LR
    G1[SonarLint - local] --> G2[Unit tests - CI]
    G2 --> G3[Sonar QG - CI]
    G3 --> G4[Peer review - human]
    G4 --> G5[Robot critical - CI]
    G5 --> G6[Merge]
    G6 --> G7[Nightly E2E]
    G7 --> G8[Load test - scheduled]
```

| Gate | Type | Blocks PR merge |
|------|------|-----------------|
| G1 SonarLint | Advisory / team policy | No |
| G2 Unit tests | Automated | Yes |
| G3 Sonar QG | Automated | Yes |
| G4 Peer review | Human | Yes |
| G5 Robot `@critical` | Automated | Configurable |
| G6 Merge | — | — |
| G7 Nightly E2E | Automated | No (alerts) |
| G8 Load test | Automated | Release only (optional) |

## SDLC context (four stages from slide)

```mermaid
flowchart LR
    S1[Requirement and Design] --> S2[Solution]
    S2 --> S3[Development and Test]
    S3 --> S4[Launch and Monitor]

    style S3 fill:#1565c0,color:#fff,stroke:#0d47a1,stroke-width:3px
```

**Current program focus:** Stage 3 (Development & Test).

## Related documents

- [sub-workflows.md](sub-workflows.md)
- [../sequences/pr-merge-happy-path.md](../sequences/pr-merge-happy-path.md)
- [../plan/implementation-plan.md](../plan/implementation-plan.md)
