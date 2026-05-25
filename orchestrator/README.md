# Orchestrator

| Script | Bước | Mô tả |
|--------|------|--------|
| `run_code_slice.py` | C | Code gen + validate |
| `run_robot_slice.py` | D | Robot gen + validate |
| `run_release_pipeline.py` | E | Test → self-heal → PR → @mentor |

## Bước E

```bash
npm run ai:release-pipeline -- --branch feature/xxx --ticket learn-005 --dry-run
```

Chi tiết: [docs/dev/release-pipeline.md](../docs/dev/release-pipeline.md).
