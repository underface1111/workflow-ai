# Architecture Decision Records (ADR)

Summary decisions for the GenAI-integrated Development & Test workflow.

---

## ADR-01: Mandatory SonarQube PR quality gate

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Context** | Slide shows high maturity for Code Quality; PR integration is explicit |
| **Decision** | Every PR runs SonarQube analysis; merge blocked on quality gate failure |
| **Consequences** | Requires SonarQube server, scanner in CI, coverage from unit tests |
| **Alternatives rejected** | IDE-only checks (no enforceable gate on PR) |

---

## ADR-02: Robot Framework for E2E; stack-native framework for unit tests

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Context** | ~10% critical cases automated with Robot; need growth to 50%+ |
| **Decision** | Robot for critical functional E2E; Jest/Pytest/JUnit/etc. for unit/integration in CI |
| **Consequences** | Two test stacks to maintain; clear tagging (`@critical`) for PR scope |
| **Alternatives rejected** | Cypress-only (slide specifies Robot); manual-only E2E at scale |

---

## ADR-03: E2E `@critical` on PR; full suite nightly

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Context** | KPI ~70% merge in <1 business day conflicts with full E2E on every PR |
| **Decision** | PR pipelines run only `@critical` Robot suites; full regression on `main` nightly |
| **Consequences** | Risk of undetected regressions in non-critical paths until nightly; requires triage process |
| **Mitigation** | Flake tracking; expand `@critical` set gradually with coverage metrics |

---

## ADR-04: Load tests on dedicated performance environment

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Context** | ~70% journeys tested at 20k+ simulated users |
| **Decision** | Load tests (k6/JMeter) run only in Perf env; never against shared Test/Dev |
| **Consequences** | Extra environment cost; release cadence tied to scheduled load windows |
| **Alternatives rejected** | Load test in Test env (destabilizes E2E and dev work) |

---

## ADR-05: GenAI assists development; does not auto-merge

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Context** | GitHub Copilot enabled with DevEx; ~80% merge-ready after peer review |
| **Decision** | Copilot/Cursor under coding standards and security policy; human review required |
| **Consequences** | Training on prompt hygiene; review checklist includes AI-generated code |
| **Alternatives rejected** | Auto-merge on green CI (insufficient for slide KPI on review readiness) |

---

## ADR-06: Azure DevOps as orchestration and traceability hub

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Context** | Slide references ADO component standardization |
| **Decision** | Pipelines, test plans, work items, and PR policies live in ADO |
| **Consequences** | Teams using GitHub-only need equivalent mapping (Actions, Issues, branch protection) |
| **Note** | ADR stands for Azure DevOps; adapt tool names if stack differs |

---

## ADR index

| ID | Title |
|----|-------|
| ADR-01 | SonarQube PR quality gate |
| ADR-02 | Robot E2E + native unit tests |
| ADR-03 | Critical E2E on PR, full nightly |
| ADR-04 | Dedicated performance environment |
| ADR-05 | GenAI without auto-merge |
| ADR-06 | ADO orchestration |
