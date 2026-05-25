# Robot Framework E2E (API)

Steel-thread tests against the Node POC using **RequestsLibrary** (no browser required).

## Prerequisites

- Python 3.10+
- POC API running: `npm start` (default `http://localhost:3000`)

## Setup

```bash
cd tests/e2e-robot
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## Run critical suites (PR scope)

```bash
robot --outputdir ../../robot-results --include critical suites/critical
```

## Run from repo root (helper)

```bash
npm run start
# other terminal:
npm run test:e2e
```

Add to root `package.json` if using npm script — see root README.

## ADO / CI

Publish `robot-results/output.xml` with the **Publish Test Results** task (see `.ado/pipelines/ci.yml`).
