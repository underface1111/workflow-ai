# Bước A — Branch protection & required checks

Làm trên GitHub sau khi PR `learn/practice` → `main` CI xanh.

## A1 — Branch protection.

1. Repo **Settings** → **Branches** → **Add branch protection rule**
2. Branch name pattern: `main`
3. Bật:
   - **Require a pull request before merging**
   - **Require approvals** (1)
   - **Do not allow bypassing the above settings** (khuyến nghị khi học)
4. (Tùy chọn) **Require conversation resolution before merging**

## A2 — Required status checks

Trong cùng rule (hoặc **Rulesets** nếu org dùng rulesets):

1. **Require status checks to pass before merging**
2. **Require branches to be up to date before merging**
3. Chọn checks (tên job trong [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)):

| Check name (GHA job) | Workflow |
|----------------------|----------|
| `build-test-sonar` | CI — unit, validate B4, Sonar |
| `e2e-robot` | CI — Robot `@critical` |

Nếu không thấy tên job: merge một PR có CI chạy xong trước, rồi quay lại Settings và chọn lại.

## A3 — SonarCloud Quality Gate

1. [SonarCloud](https://sonarcloud.io) → project `workflow-ai-poc`
2. **Quality Gate** → dùng default hoặc **Sonar way**
3. **New Code** definition: Previous version (khuyến nghị cho PR)
4. Tắt **Automatic Analysis** (chỉ CI scan) — xem [sonarlint-cursor.md](sonarlint-cursor.md)
5. Trên PR: SonarCloud bot / check phải **Passed** trước merge (nếu đã gắn vào required checks)

## Mở PR (nếu chưa có)

```text
https://github.com/underface1111/workflow-ai/compare/main...learn/practice
```

Title gợi ý: `feat: Bước B AI test agent + B4 validate in CI`

## Exit Bước A

- [ ] PR merge vào `main` với 1 approval
- [ ] Lần push sau vào `main` bị chặn (phải qua PR)
- [ ] CI fail → không merge được
