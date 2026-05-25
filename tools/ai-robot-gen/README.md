# AI Robot E2E Agent (Bước D)

Sinh **Robot Framework** suites trong `tests/e2e-robot/suites/generated/` — tag **`generated`**, không thay **`critical`**.

## Setup

```bash
python -m pip install -r tools/ai-robot-gen/requirements.txt
pip install -r tests/e2e-robot/requirements.txt
npm start   # terminal khác
```

## LEARN-004

```bash
npm run ai:robot-gen:learn-004
npm run ai:robot-validate:only    # CI: cấu trúc
npm run test:e2e:generated        # chạy Robot generated
```

Hoặc một lệnh:

```bash
npm run ai:robot-slice
```

## Tags (D2)

| Tag | CI | Mục đích |
|-----|-----|----------|
| `critical` | `e2e-robot` job | Steel thread ổn định |
| `generated` | bước riêng trong CI | Suite AI sinh, review trước merge |

## Review (D3)

Đọc diff `*.robot` generated trước khi merge — giống B5 unit tests.
