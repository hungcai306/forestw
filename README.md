# Hue ForestWatch — Render Production Starter

Kiến trúc triển khai:

- `hue-forestwatch-web`: React/Vite Static Site.
- `hue-forestwatch-api`: FastAPI Web Service.
- `hue-forestwatch-db`: PostgreSQL/PostGIS.

## Triển khai

1. Đưa toàn bộ mã nguồn lên GitHub.
2. Render → **New** → **Blueprint**.
3. Chọn repository; Render đọc `render.yaml`.
4. Nhập `SADMIN_PASSWORD` khi được yêu cầu.
5. Mở `https://hue-forestwatch-web.onrender.com`.

Tài khoản mặc định: `sadmin`.

## Địa chỉ dịch vụ

- Web: `https://hue-forestwatch-web.onrender.com`
- API: `https://hue-forestwatch-api.onrender.com`
- Swagger: `https://hue-forestwatch-api.onrender.com/docs`

## Chạy local

```bash
docker compose up
```

- Web: http://localhost:5173
- API: http://localhost:8000

## Lưu ý vận hành

- Google Satellite và lớp nhãn đang sử dụng URL tile không cần API key; cần rà soát điều khoản Google trước khi dùng chính thức.
- Render Postgres Free hết hạn sau 30 ngày; dữ liệu nghiệp vụ thật nên dùng gói trả phí và cấu hình sao lưu.
- Khi đổi tên dịch vụ/domain, cập nhật `CORS_ORIGINS` và `VITE_API_URL` trong Render.
