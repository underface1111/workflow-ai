# Sequence: Metrics Collection

ETL from Git, SonarQube, and ADO into the program KPI dashboard.

## Diagram

```mermaid
sequenceDiagram
    autonumber
    participant Git as Git / ADO Repos
    participant Sonar as SonarQube API
    participant ADO as ADO Analytics
    participant ETL as Metrics ETL (scheduled)
    participant BI as KPI Dashboard
    participant Lead as Engineering Lead

    loop Hourly or Daily
        ETL->>Git: PR cycle time, merge-ready signals
        ETL->>Sonar: Coverage by project
        ETL->>ADO: E2E pass rate, automation count
    end
    ETL->>BI: Aggregate KPIs
    Lead->>BI: Review program maturity
    BI-->>Lead: Heatmap vs targets (80/90/70/10/70)
```

## Data sources

| KPI | Primary source | Suggested query / signal |
|-----|----------------|---------------------------|
| Merge-ready after review | ADO / Git PR API | PRs approved without `changes requested` after first review |
| Coverage >50% | SonarQube API | `coverage` measure per project |
| Merge <1 business day | Git / ADO | `mergedAt - createdAt` in business hours |
| Critical automated % | ADO Test Plans | `automated_critical / total_critical` |
| Load journey coverage | Load registry DB | `journeys_passed_20k / total_happy_path` |

## Dashboard views

1. **Program heatmap** — maturity by SDLC stage (matches slide legend)
2. **Squad drill-down** — PR cycle time, review rounds, Sonar failures
3. **Test automation trend** — Robot case count over sprints
4. **Load coverage** — steel threads and last 20k run status

## Ritual

- **Weekly:** squad lead reviews squad tile
- **Bi-weekly:** program review with engineering leadership
- **Monthly:** adjust quality gate thresholds and automation backlog

## Related

- [../metrics/kpi-definitions.md](../metrics/kpi-definitions.md)
- [../plan/implementation-plan.md](../plan/implementation-plan.md)
