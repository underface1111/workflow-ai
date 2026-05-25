# Sequence: Robot Framework E2E

Deploy to test environment and run Robot suites on PR (`@critical`) and nightly (full).

## Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant Git as PR / Merge Policy
    participant CI as ADO Pipeline
    participant Dep as Deploy Task
    participant Test as Test Environment
    participant Robot as Robot Framework
    participant ADO as ADO Test Results
    participant QA as QA Engineer

    Note over Git,CI: After Sonar QG pass (and optionally in parallel with review)

    Git->>CI: PR validated - critical paths
    CI->>Dep: Deploy build to Test
    Dep->>Test: App running + test data seed
    CI->>Robot: Run suites tagged @critical
    Robot->>Test: HTTP/UI actions on journeys
    Test-->>Robot: Responses
    Robot-->>CI: JUnit or XML report

    alt E2E failed
        CI-->>Git: Block merge / failed check
        CI->>ADO: Publish failed tests
        Dev->>Robot: Fix tests or application
    else E2E passed
        CI->>ADO: Publish passed tests
        CI-->>Git: E2E check passed
        Git->>Dev: Allow merge
    end

    opt Nightly on main
        CI->>Robot: Full regression suite
        Robot->>ADO: Trend report
        QA->>ADO: Triage flakes / update manual backlog
    end
```

## Pipeline configuration notes

| Setting | PR build | Nightly |
|---------|----------|---------|
| Tags | `critical` | all suites |
| Timeout | 15–30 min | 60–120 min |
| Retry | 1 retry on flake (optional) | no auto-retry |
| Artifacts | log.html, output.xml | same + archive 30d |

## ADO integration

1. Publish test results task consumes Robot `output.xml`
2. Link test run to build number and commit SHA
3. Failed tests create bugs automatically (optional team setting)

## KPI linkage

- **% critical automated:** count automated / total critical in test plan

## Related

- [../workflow/sub-workflows.md](../workflow/sub-workflows.md#2-automated-testing-robot-framework)
- [../architecture/adr.md](../architecture/adr.md) (ADR-02, ADR-03)
