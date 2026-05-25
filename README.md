# Workflow AI — GenAI-Integrated SDLC (Node POC)

Node.js proof-of-concept for the **Development & Test** workflow: Express API, Jest unit tests, SonarQube, Robot Framework E2E (`@critical`), and k6 load script.

**Repository:** [github.com/underface1111/workflow-ai](https://github.com/underface1111/workflow-ai)  
**CI:** [GitHub Actions](https://github.com/underface1111/workflow-ai/actions) (unit → SonarCloud → Robot E2E)

```bash
git clone git@github.com:underface1111/workflow-ai.git
cd workflow-ai
npm ci
```

<!-- ci-trigger -->

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

## AI Test Agent (Bước B)

Tạm thời chưa có API key → dùng template; khi có key → `npm run ai:test-gen:llm`.

```bash
python -m pip install -r tools/ai-test-gen/requirements-validate.txt
npm run ai:test-gen           # template (đang dùng)
npm run ai:test-validate      # validate + npm test
# npm run ai:test-gen:llm    # Claude — khi có ANTHROPIC_API_KEY trong .env
```

See [tools/ai-test-gen/README.md](tools/ai-test-gen/README.md).

## AI Code Agent (Bước C)

```bash
python -m pip install -r tools/ai-code-gen/requirements.txt
npm run ai:code-slice    # LEARN-003: /health version field
```

See [tools/ai-code-gen/README.md](tools/ai-code-gen/README.md).

## AI Robot E2E (Bước D)

```bash
python -m pip install -r tools/ai-robot-gen/requirements.txt
npm run ai:robot-slice
npm run test:e2e:generated   # npm start trước
```

See [tools/ai-robot-gen/README.md](tools/ai-robot-gen/README.md).

## Release pipeline (Bước E)

```bash
npm run ai:release-pipeline -- --branch feature/my-branch --ticket learn-005 --dry-run
```

See [docs/dev/release-pipeline.md](docs/dev/release-pipeline.md).

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

1. [docs/plan/how-to-build-workflow.md](docs/plan/how-to-build-workflow.md) — **As-Is:** cách xây từng lớp (POC hiện tại)
2. [docs/plan/as-is-vs-to-be.md](docs/plan/as-is-vs-to-be.md) — so sánh với **AI Orchestrator (To-Be)**
3. [docs/plan/evolution-roadmap.md](docs/plan/evolution-roadmap.md) — bước tiếp theo A→F
4. [docs/workflow/macro-workflow.md](docs/workflow/macro-workflow.md) — luồng tổng thể
5. Chạy POC: `npm test` → PR → CI → SonarLint + `npm run test:e2e`

## Documentation

| Document | Description |
|----------|-------------|
| [docs/README.md](docs/README.md) | Full documentation index |
| [docs/plan/how-to-build-workflow.md](docs/plan/how-to-build-workflow.md) | Cách xây workflow (học tập) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | PR checklist & GenAI rules |

## SonarLint (Cursor)

Cài extension **SonarLint** và bind SonarCloud project `workflow-ai-poc`: [docs/dev/sonarlint-cursor.md](docs/dev/sonarlint-cursor.md)

## SonarCloud

| Nơi | Dùng cho |
|-----|----------|
| **GitHub Secrets** `SONAR_TOKEN`, `SONAR_HOST_URL` | CI trên mỗi PR/push (bắt buộc để scan chạy) |
| File `.env` (local, không commit) | Chỉ khi chạy `sonar-scanner` trên máy |

1. Tạo project trên [SonarCloud](https://sonarcloud.io) → import repo `underface1111/workflow-ai`
2. Khớp **Organization key** và **Project key** với `sonar-project.properties` (`sonar.organization`, `sonar.projectKey`)
3. Thêm secrets trên GitHub (không chỉ `.env`)
4. **Tắt Automatic Analysis** trên SonarCloud (bắt buộc nếu dùng CI):
   - Project → **Project Settings** → **Administration** → **Analysis Method**
   - Tắt **Automatic Analysis** (chỉ giữ phân tích qua GitHub Actions)

Nếu không tắt, CI báo lỗi: *"CI analysis while Automatic Analysis is enabled"*.

```bash
npm run test:ci
# npx sonar-scanner   # cần sonar-scanner CLI + .env local
```

Coverage: `coverage/lcov.info`
