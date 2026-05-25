# Deployment Topology

Environment layout and promotion paths for Development & Test workloads.

## Per-PR flow

```mermaid
flowchart LR
    PR[PR Branch] --> CI[CI Agent Pool]
    CI --> ART[Build Artifacts]
    ART --> TEST[(Test Environment)]
    TEST --> E2E[Robot E2E - critical on PR]
```

## Scheduled and release flows

```mermaid
flowchart LR
    TEST[(Test Environment)] --> NIGHTLY[Nightly Full E2E on main]
    PERF[(Performance Environment)] --> LOAD[Load Test 20k VUs]
    NIGHTLY --> REPORT[ADO Test Reports]
    LOAD --> METRICS[APM and KPI Dashboard]
```

## Future: Launch and Monitor (low maturity on baseline slide)

```mermaid
flowchart LR
    TEST[(Test Environment)] --> STAGE[Staging]
    STAGE --> PROD[Production]
    PROD --> MON[SLA / APM / Incident Management]
```

## Environment characteristics

| Environment | Purpose | Deploy trigger | Notes |
|-------------|---------|----------------|-------|
| **Dev** | Local and early integration | Developer machine | SonarLint only; optional local unit tests |
| **Test / QA** | PR validation, Robot E2E | Every PR (after QG) + on merge | Stable test data; seeded identities |
| **Performance** | Steel Thread load tests | Scheduled / pre-release | Isolated; no shared resources with Test |
| **Staging** | Pre-prod validation | Release branch | Phase 3+ |
| **Production** | Live workloads | Approved release | Phase 3+; ties to Launch & Monitor |

## Pipeline stage mapping (ADO)

| Stage | Runs on | Blocks merge |
|-------|---------|--------------|
| Build + unit | PR, main | Yes |
| SonarQube scan + QG | PR, main | Yes |
| Deploy to test | PR (if critical paths), main | PR: optional policy |
| Robot `@critical` | PR | Yes (if policy enabled) |
| Robot full suite | Nightly on main | No (alerting) |
| Load test | Weekly / release | No (release gate optional) |

## Related documents

- [logical-architecture.md](logical-architecture.md)
- [../workflow/macro-workflow.md](../workflow/macro-workflow.md)
- [../sequences/robot-e2e.md](../sequences/robot-e2e.md)
