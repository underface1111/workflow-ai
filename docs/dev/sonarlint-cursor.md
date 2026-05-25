# SonarLint trên Cursor

Cursor dùng nền VS Code → cài extension **SonarLint** (SonarSource) và **Connected Mode** với SonarCloud project `workflow-ai-poc`.

## 1. Cài extension

1. Mở Cursor → **Extensions** (`Ctrl+Shift+X`)
2. Tìm **SonarLint** (publisher: SonarSource)
3. **Install**

Hoặc chấp nhận gợi ý khi mở repo (file `.vscode/extensions.json`).

## 2. Kết nối SonarCloud (một lần / máy)

1. `Ctrl+Shift+P` → **SonarLint: Add SonarCloud Connection**
2. Chọn / tạo connection id: `sonarcloud` (khớp `.vscode/settings.json`)
3. Dán **User Token** từ SonarCloud:
   - https://sonarcloud.io/account/security → Generate Tokens
   - **Không** commit token vào git (chỉ lưu trong Cursor user settings)

## 3. Bind project (workspace)

Repo đã cấu hình sẵn trong `.vscode/settings.json`:

| Setting | Giá trị |
|---------|--------|
| Organization | `underface1111` |
| Project key | `workflow-ai-poc` |
| Connection id | `sonarcloud` |

Nếu chưa tự bind:

- `Ctrl+Shift+P` → **SonarLint: Bind to SonarCloud Project**
- Chọn organization `underface1111` → project `workflow-ai-poc`

## 4. Dùng hàng ngày

1. Mở file trong `src/` (vd. `src/app.js`)
2. Xem **Problems** (`Ctrl+Shift+M`) — issue từ SonarLint
3. Hover issue → xem rule và gợi ý sửa
4. Sửa trên máy → `npm test` → push → CI SonarCloud xác nhận lại

## 5. SonarLint vs CI

```text
SonarLint (IDE)     → phản hồi ngay khi code
npm test            → unit + coverage local
GitHub Actions      → SonarCloud scan + Quality Gate trên PR
```

SonarLint **không thay** Quality Gate trên PR; giúp ít fail CI hơn.

## 6. Lỗi thường gặp

| Triệu chứng | Cách xử lý |
|-------------|------------|
| Không thấy issue | Bind đúng project; mở file trong `sonar.sources` (`src/`) |
| Connection failed | Token hết hạn → tạo token mới, Add Connection lại |
| Rule khác CI | Connected Mode dùng cùng Quality Profile SonarCloud |
| Automatic Analysis | Trên SonarCloud phải **tắt** nếu dùng CI scanner (xem README) |

## 7. Liên quan

- `sonar-project.properties` — cấu hình CI scanner
- `README.md` — secrets `SONAR_TOKEN`, `SONAR_HOST_URL` trên GitHub
