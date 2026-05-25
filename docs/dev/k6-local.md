# k6 load test — local (Bước 2)

Script: [`perf/k6/steel_thread.js`](../../perf/k6/steel_thread.js) — login → catalog → cart → checkout.

## Prerequisites

- API running: `npm start` → http://localhost:3000
- **k6** installed **or** Docker Desktop running

## Option A — k6 CLI (Windows)

```powershell
choco install k6
# or: winget install k6 --source winget
npm start
k6 run perf/k6/steel_thread.js
```

Smoke (ngắn):

```powershell
k6 run --vus 2 --duration 15s perf/k6/steel_thread.js
```

## Option B — Docker

```powershell
npm start
docker run --rm -e BASE_URL=http://host.docker.internal:3000 `
  -v ${PWD}/perf/k6:/scripts grafana/k6 run /scripts/steel_thread.js
```

## Verify API without k6

```powershell
Invoke-WebRequest http://localhost:3000/health -UseBasicParsing
```

Exit: thresholds pass (`p(95)<500`, `http_req_failed<1%`, `checks>99%`).

**Verified (Docker):** 2697 iterations, 0 failed requests, p(95) latency ~1.32ms, all checks 100%.
