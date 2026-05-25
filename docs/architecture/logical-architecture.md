# Logical Architecture

Container-level view of the GenAI-integrated **Development & Test** platform.

## Container diagram

```mermaid
flowchart TB
    subgraph people["People"]
        DEV[Developer]
        REV[Peer Reviewer]
        QA[QA Engineer]
        PERF[Performance Engineer]
    end

    subgraph devtools["Developer Tools"]
        IDE[IDE + SonarLint]
        GENAI[GitHub Copilot / Cursor]
    end

    subgraph scm["Source Control"]
        GIT[Git Repository]
        PR[Pull Request]
    end

    subgraph quality["Quality Platform"]
        SONAR[SonarQube Server]
        QG[Quality Gate]
    end

    subgraph cicd["CI/CD - ADO Pipelines"]
        BUILD[Build and Unit Test]
        SCAN[Sonar Scanner]
        DEPLOY[Deploy to Test Env]
        E2E[Robot Framework Runner]
        LOAD[Load Test Runner - scheduled]
    end

    subgraph testassets["Test Assets"]
        ROBOT[Robot Suites / Keywords]
        K6[k6 or JMeter Scripts]
        MANUAL[ADO Test Plans - Manual]
    end

    subgraph runtime["Environments"]
        DEVENV[Dev]
        TESTENV[Test / QA]
        PERFENV[Performance]
    end

    subgraph observability["Observability and Metrics"]
        ADO_MET[ADO Analytics]
        SONAR_API[Sonar API]
        DASH[KPI Dashboard]
    end

    DEV --> IDE
    DEV --> GENAI
    IDE --> GIT
    GENAI --> GIT
    GIT --> PR
    PR --> BUILD
    BUILD --> SCAN
    SCAN --> SONAR
    SONAR --> QG
    QG -->|pass| DEPLOY
    DEPLOY --> TESTENV
    TESTENV --> E2E
    ROBOT --> E2E
    E2E -->|results| ADO_MET
    PERFENV --> LOAD
    K6 --> LOAD
    REV --> PR
    QA --> ROBOT
    QA --> MANUAL
    PERF --> K6
    ADO_MET --> DASH
    SONAR_API --> DASH
```

## Component responsibilities

| Component | Responsibility |
|-----------|----------------|
| **IDE + SonarLint** | Shift-left: bugs, code smells, security issues before commit |
| **GenAI (Copilot / Cursor)** | Generate code and tests per standards; does not replace gates |
| **Git + PR** | Single path to integration; audit trail |
| **SonarQube + Quality Gate** | Coverage, duplications, vulnerabilities on PR |
| **CI build + unit tests** | Fast feedback (target <10 minutes) |
| **Robot + test environment** | E2E critical journeys; JUnit/XML to ADO |
| **Load runner + perf environment** | Steel Thread scenarios; scale to 20k+ VUs |
| **ADO test plans** | Manual test traceability and automation backlog |
| **KPI dashboard** | Merge time, coverage, automation %, load coverage |

## Data and integration flows

| Flow | From → To | Purpose |
|------|-----------|---------|
| Code diff | Git → SonarQube | Analyze new/changed code |
| Coverage | Test runner → SonarQube | Quality gate enforcement |
| E2E results | Robot → ADO Tests | Pass/fail trends |
| Work items | ADO → PR description | Requirement traceability |
| Program metrics | Git / ADO / Sonar APIs → Dashboard | KPI reporting |

## Security and compliance constraints

- Secrets only in ADO variable groups or Azure Key Vault
- GenAI: no PII or secrets in prompts; policy approved by Legal/Security
- SonarQube: block critical/high vulnerabilities on PR merge
- Performance environment: anonymized data; isolated network; no production credentials

## Related documents

- [deployment-topology.md](deployment-topology.md)
- [adr.md](adr.md)
- [../sequences/pr-merge-happy-path.md](../sequences/pr-merge-happy-path.md)
