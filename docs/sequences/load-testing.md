# Sequence: Load Testing — Steel Thread

Steel Thread Phase 2 with ramp to 20k+ simulated users and architecture validation.

## Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Perf as Performance Engineer
    participant Arch as Architect
    participant CI as Release / Scheduled Pipeline
    participant PerfEnv as Performance Environment
    participant k6 as k6 / JMeter
    participant APM as APM / Metrics Store
    participant Dash as KPI Dashboard

    Perf->>Arch: Define steel thread journeys
    Arch-->>Perf: SLA targets (p95, error rate)

    Perf->>k6: Author scripts + thresholds
    Perf->>CI: Register scheduled run

    CI->>PerfEnv: Deploy release candidate
    CI->>k6: Start ramp 0 to 20k VUs
    loop Each journey scenario
        k6->>PerfEnv: Simulate user flow
        PerfEnv-->>k6: Latency and status codes
    end
    k6->>APM: Export metrics
    k6-->>CI: Pass or fail vs thresholds

    alt SLA breached
        CI-->>Perf: Fail pipeline
        Perf->>Arch: Architecture validation session
        Arch-->>Perf: Scaling or design actions
    else SLA met
        CI-->>Perf: Record journey tested
        Perf->>Dash: Update load coverage KPI
        Arch->>Dash: Sign-off validation
    end
```

## Example thresholds (k6)

```javascript
// Illustrative — tune per journey
export const options = {
  stages: [
    { duration: '10m', target: 5000 },
    { duration: '20m', target: 20000 },
    { duration: '10m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.001'],
  },
};
```

## Steel thread registry (recommended fields)

| Field | Description |
|-------|-------------|
| `journey_id` | Unique ID matching test plan |
| `phase` | 1 (baseline) or 2 (20k+) |
| `last_run` | ISO date |
| `max_vus` | Peak virtual users |
| `p95_ms` | 95th percentile latency |
| `error_rate` | Failed requests / total |
| `arch_signoff` | Y/N + reviewer |

## KPI linkage

- **~70% happy-path load-tested at 20k+:** journeys with successful Phase 2 run / total happy-path journeys

## Related

- [../workflow/sub-workflows.md](../workflow/sub-workflows.md#3-load-testing-steel-thread)
- [../architecture/deployment-topology.md](../architecture/deployment-topology.md)
