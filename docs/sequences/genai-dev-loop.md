# Sequence: GenAI-Assisted Development Loop

GitHub Copilot or Cursor assists coding; quality gates remain human and automated.

## Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant GenAI as Copilot / Cursor
    participant Rules as Coding Standards / Rules
    participant IDE as SonarLint
    participant Git as Git

    Dev->>Rules: Load squad standards
    Dev->>GenAI: Prompt with context + rules
    GenAI-->>Dev: Code suggestion
    Dev->>Dev: Review and adapt suggestion
    Dev->>IDE: Analyze changed files
    IDE-->>Dev: Quality and security hints

    alt Issues found
        Dev->>GenAI: Refine with constraints
    else Clean enough
        Dev->>Dev: Write and run unit tests
        Dev->>Git: Commit (no secrets policy)
    end

    Note over Dev,Git: GenAI stops at commit. Sonar QG and peer review still required.
```

## Guardrails (DevEx)

| Rule | Rationale |
|------|-----------|
| No secrets in prompts or commits | Security policy |
| Human reviews all AI-generated logic | ~80% merge-ready KPI |
| Unit tests required for new behavior | Coverage and regression |
| Follow squad naming and structure | Sonar and review consistency |
| Do not disable Sonar rules to pass gate | Quality over speed |

## Recommended rule sources

- `CONTRIBUTING.md` — human-readable standards
- `.cursor/rules/` or Copilot instructions — machine-readable for GenAI
- Sonar quality profile — enforced on PR

## Boundary

```mermaid
flowchart LR
    GENAI[GenAI assists] --> COMMIT[Commit]
    COMMIT --> SONAR[Sonar QG - automated]
    SONAR --> HUMAN[Peer review - human]
    HUMAN --> MERGE[Merge]

    style GENAI fill:#e8f5e9
    style SONAR fill:#e3f2fd
    style HUMAN fill:#fff3e0
```

## Related

- [../architecture/adr.md](../architecture/adr.md) (ADR-05)
- [pr-merge-happy-path.md](pr-merge-happy-path.md)
