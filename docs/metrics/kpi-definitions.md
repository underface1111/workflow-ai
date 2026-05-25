# KPI Definitions

Measurable definitions for Development & Test metrics from the BankCo GenAI SDLC slide.

## Summary table

| ID | KPI (slide) | Baseline | 12-month target | Owner |
|----|-------------|----------|-----------------|-------|
| K1 | Merge-ready after peer review | ~80% | ≥85% | Tech Leads |
| K2 | Repos with >50% test coverage | ~90% | ≥95% repos | Quality Lead |
| K3 | Changes merged in <1 business day | ~70% | ≥75% | Engineering Lead |
| K4 | Critical cases automated (Robot) | ~10% | ≥50% | QA Lead |
| K5 | Happy-path load-tested (20k+ users) | ~70% | ≥85% | Performance Eng |

---

## K1: Merge-ready after peer review

**Definition:** Percentage of PRs that receive approval without a `changes requested` review cycle after the first human review pass.

**Formula:**

```
K1 = (PRs approved on first review round / PRs with at least one review) × 100
```

**Data source:** ADO/Git pull request reviews API

**Notes:**

- Exclude draft PRs and abandoned PRs
- "Merge-ready" may use label `merge-ready` if team adopts explicit workflow

---

## K2: Repositories with >50% test coverage

**Definition:** Percentage of SonarQube-registered projects where overall line coverage exceeds 50%.

**Formula:**

```
K2 = (projects with coverage > 50% / total active projects) × 100
```

**Data source:** SonarQube Web API — `measures/component` with metric `coverage`

**Notes:**

- Prefer **overall** coverage for portfolio KPI; use **new code** coverage on PR gate
- New repos included after first successful Sonar analysis

---

## K3: Code changes merged in less than one business day

**Definition:** Percentage of merged PRs where elapsed time from PR creation to merge is within one business day (team timezone, excluding weekends/holidays).

**Formula:**

```
K3 = (PRs merged within 1 business day / PRs merged in period) × 100
```

**Data source:** Git / ADO PR timestamps

**Notes:**

- Business day = configurable calendar (e.g. 8h or 24h wall-clock — document team choice)
- Large PRs may be excluded by size label for fair measurement

---

## K4: Critical functional test cases automated (Robot)

**Definition:** Percentage of test cases marked **critical** in ADO Test Plans that are executed by Robot Framework in CI.

**Formula:**

```
K4 = (critical test cases with automated Robot implementation / total critical test cases) × 100
```

**Data source:** ADO Test Plans + Robot suite inventory (tag or case ID mapping)

**Notes:**

- Baseline ~10% on slide — primary growth metric for program
- Manual cases remain tracked until automated

---

## K5: Happy-path journeys load-tested at 20k+ simulated users

**Definition:** Percentage of defined happy-path user journeys that completed a successful Phase 2 load test with peak load ≥20,000 virtual users within the reporting window (e.g. last 90 days).

**Formula:**

```
K5 = (journeys with successful 20k+ run / total catalogued happy-path journeys) × 100
```

**Data source:** Load test registry + CI/Perf pipeline results + APM exports

**Notes:**

- Journey catalog maintained by Performance + Architecture
- Failed runs do not count until a subsequent successful run

---

## Maturity heatmap (program reporting)

Map sub-areas to slide legend (Low → High):

| Sub-area | Baseline maturity | Investment priority |
|----------|-------------------|---------------------|
| Code Development | Medium | Medium |
| Code Review | High | Maintain |
| Code Quality | High | Maintain |
| Automated Testing | Low (~10% K4) | **High** |
| Load Testing | High (~70% K5) | Medium (expand catalog) |

---

## Reporting cadence

| Report | Audience | Frequency |
|--------|----------|-----------|
| Squad tile | Tech lead | Weekly |
| Development & Test scorecard | Engineering leadership | Bi-weekly |
| Full SDLC heatmap | Program / management | Monthly |

## Related

- [../sequences/metrics-collection.md](../sequences/metrics-collection.md)
- [../plan/implementation-plan.md](../plan/implementation-plan.md)
