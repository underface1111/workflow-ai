# Workflow AI — GenAI-Integrated SDLC (Node POC)

Node.js proof-of-concept for the **Development & Test** workflow: Express API, Jest unit tests, SonarQube, Robot Framework E2E (`@critical`), and k6 load script.

**Repository:** [github.com/underface1111/workflow-ai](https://github.com/underface1111/workflow-ai)

```bash
git clone git@github.com:underface1111/workflow-ai.git
cd workflow-ai
npm ci
```

## Quick start

```bash
npm ci
npm test              # unit tests + coverage (≥50% threshold)
npm start             # http://localhost:3000
```

**Demo login:** `demo@bankco.local` / `demo123`

### Steel-thread API

```http
POST /auth/login     → { token }
GET  /catalog        → Bearer token
POST /cart/items     → { skuId, quantity }
POST /checkout       → { orderId, status: "confirmed" }
GET  /health         → public
```

## E2E (Robot Framework)

```bash
npm start
# other terminal:
cd tests/e2e-robot && pip install -r requirements.txt
npm run test:e2e
```

See [tests/e2e-robot/README.md](tests/e2e-robot/README.md).

## Load test (k6)

```bash
npm start
k6 run perf/k6/steel_thread.js
```

## CI

| Platform | File |
|----------|------|
| GitHub Actions | [.github/workflows/ci.yml](.github/workflows/ci.yml) |
| Azure DevOps | [.ado/pipelines/ci.yml](.ado/pipelines/ci.yml) |

Set `SONAR_TOKEN` + `SONAR_HOST_URL` secrets for SonarQube scan (optional locally).

## Project layout

```
workflow-ai/
├── src/                 # Express app
├── tests/unit/          # Jest
├── tests/e2e-robot/     # Robot @critical
├── perf/k6/             # Steel thread load
├── .ado/pipelines/      # ADO template
├── .github/workflows/   # GitHub CI
├── docs/                # Architecture & workflow docs
├── sonar-project.properties
└── CONTRIBUTING.md
```

## Học workflow — đọc theo thứ tự

1. [docs/plan/how-to-build-workflow.md](docs/plan/how-to-build-workflow.md) — **cách xây từng lớp** (không theo tuần)
2. [docs/workflow/macro-workflow.md](docs/workflow/macro-workflow.md) — luồng tổng thể
3. Chạy POC: `npm test` → PR → xem CI → (tùy chọn) Sonar + `npm run test:e2e`

## Documentation

| Document | Description |
|----------|-------------|
| [docs/README.md](docs/README.md) | Full documentation index |
| [docs/plan/how-to-build-workflow.md](docs/plan/how-to-build-workflow.md) | Cách xây workflow (học tập) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | PR checklist & GenAI rules |

## SonarQube (local)

```bash
npm run test:ci
# sonar-scanner -Dsonar.host.url=... -Dsonar.token=...
```

Coverage report: `coverage/lcov.info`
