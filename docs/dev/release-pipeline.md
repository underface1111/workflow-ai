# Bước E — Release pipeline (auto PR + self-heal)

**Không auto-merge.** Chỉ mở PR + comment khi test pass.

## Local (dry-run)

```powershell
git checkout -b feature/learn-005-demo
# ... changes ...
git push -u origin feature/learn-005-demo

npm ci
npm run ai:release-pipeline -- --branch feature/learn-005-demo --ticket learn-005 --dry-run
```

## Local (thật — cần token)

```powershell
$env:GITHUB_TOKEN = "ghp_..."
$env:MENTOR_GITHUB_LOGIN = "your-github-username"
npm run ai:release-pipeline -- --branch feature/learn-005-demo --ticket learn-005
```

## GitHub Actions

**Actions** → **Release Pipeline** → Run workflow:

- `branch`: tên branch đã push (vd. `feature/learn-004-robot-e2e`)
- `ticket`: `learn-005`
- `create_pr`: true

Workflow chạy test + self-heal trên runner; nếu pass và `create_pr=true` → mở PR + @mentor.

## Self-heal

- Đọc `coverage/junit.xml` sau `npm test`
- Tối đa **3** lần template fix (`orchestrator/self_heal.py`)
- LLM heal: chưa bật (có thể thêm sau)

## Metrics (E4)

`orchestrator/out/metrics-*.json` — thời gian, số lần heal, PR URL.
