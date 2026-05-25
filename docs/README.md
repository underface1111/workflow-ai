# Documentation Index

GenAI-integrated **Software Development Lifecycle (SDLC)** with focus on **Development & Test**, based on the BankCo maturity model (Q4'24).

## Overview

| Stage | Maturity (baseline) | Program focus |
|-------|---------------------|---------------|
| Requirement & Design | Low | Out of initial scope |
| Solution / Technical Debt | Low | Out of initial scope |
| **Development & Test** | Mixed (Review/Quality/Load high; Automated Testing low) | **Primary** |
| Launch & Monitor | Low | Phase 3+ linkage |

Caption from source slide: *GenAI integrated workflow across software development lifecycle.*

## Document map

### Plan

- [how-to-build-workflow.md](plan/how-to-build-workflow.md) — **Cách xây từng lớp workflow** (học tập, không timeline)
- [implementation-plan.md](plan/implementation-plan.md) — Redirect (nội dung theo tuần đã gỡ)

### Architecture

- [logical-architecture.md](architecture/logical-architecture.md) — Container diagram, responsibilities, security
- [deployment-topology.md](architecture/deployment-topology.md) — Dev / Test / Perf / Prod paths
- [adr.md](architecture/adr.md) — Architecture decision records

### Workflow

- [macro-workflow.md](workflow/macro-workflow.md) — Full Development & Test flowchart
- [sub-workflows.md](workflow/sub-workflows.md) — Code quality, Robot, load testing details

### Sequence diagrams

- [pr-merge-happy-path.md](sequences/pr-merge-happy-path.md)
- [robot-e2e.md](sequences/robot-e2e.md)
- [load-testing.md](sequences/load-testing.md)
- [genai-dev-loop.md](sequences/genai-dev-loop.md)
- [metrics-collection.md](sequences/metrics-collection.md)

### Metrics

- [kpi-definitions.md](metrics/kpi-definitions.md) — KPI formulas and data sources

## Maturity priority (Development & Test)

```mermaid
quadrantChart
    title Development and Test Maturity Targets
    x Low Maturity
    x High Maturity
    y Low Investment Priority
    y High Investment Priority
    Code Review: [0.85, 0.7]
    Code Quality: [0.85, 0.7]
    Load Testing: [0.8, 0.6]
    Code Development: [0.55, 0.8]
    Automated Testing: [0.2, 0.95]
```

**Invest first in Automated Testing** (Robot ~10% baseline) while **maintaining** Code Review, Code Quality, and Load Testing maturity.
