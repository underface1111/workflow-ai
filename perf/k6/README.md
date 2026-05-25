# Load tests (k6)

Pilot script for **Steel Thread** — scale to 20k VUs in Perf env per program plan.

## Prerequisites

Install [k6](https://k6.io/docs/get-started/installation/).

## Run locally (POC scale)

```bash
npm start
k6 run perf/k6/steel_thread.js
```

## Perf environment (20k+ VUs)

Use `perf/k6/steel_thread_20k.js` pattern from docs — run only in isolated Perf env.

```bash
k6 run -e BASE_URL=https://perf.example.com perf/k6/steel_thread.js
```
