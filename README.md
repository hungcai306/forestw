# Hue ForestWatch — Render-ready starter

Monorepo MVP cho hệ thống giám sát biến động rừng TP Huế, quản trị 5 cấp và chính quyền địa phương 2 cấp.

## Thành phần có sẵn

- FastAPI + PostgreSQL/PostGIS.
- React + TypeScript + OpenLayers.
- JWT, đăng ký/đăng nhập, phê duyệt tài khoản.
- Vai trò: `SADMIN`, `ADMIN`, `MODERATOR`, `SUSER`, `USER`.
- Phạm vi quyền theo nhóm, trạm, mã xã/phường và loại rừng.
- Đồng bộ danh mục xã/phường qua adapter API `34tinhthanh.com`.
- Health check, Swagger API và Render Blueprint.
- Giao diện bản đồ khởi tạo tại TP Huế với Google Satellite và lớp nhãn Google.

## Deploy lên Render

1. Tạo repository GitHub và đẩy toàn bộ thư mục này lên nhánh `main`.
2. Trong Render chọn **New → Blueprint**, kết nối repository. Render mặc định đọc `render.yaml` ở thư mục gốc.
3. Nhập các biến được yêu cầu:
   - `SADMIN_EMAIL`: email Tổng Quản trị viên.
   - `SADMIN_PASSWORD`: mật khẩu ban đầu, tối thiểu 8 ký tự.
4. Chọn **Deploy Blueprint**.
5. Sau khi deploy, truy cập URL dịch vụ. Swagger tại `/docs`; health check tại `/api/v1/health`.
6. Đăng nhập bằng tài khoản SAdmin đã nhập ở bước 3 và đổi mật khẩu khi bổ sung module hồ sơ cá nhân.

> Render Free phù hợp thử nghiệm, không nên dùng cho dữ liệu nhà nước hoặc sản xuất. Chuyển web service và PostgreSQL sang gói trả phí, bật backup và giới hạn truy cập trước khi vận hành chính thức.

## Chạy cục bộ

```bash
docker compose up --build
```

Mở `http://localhost:8000`. Tài khoản mặc định cục bộ:

```text
sadmin@example.gov.vn
ChangeMe123!
```

## API chính

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
GET  /api/v1/admin/users/pending
POST /api/v1/admin/users/{id}/approve
POST /api/v1/admin/users/{id}/scope
GET  /api/v1/administrative/wards
POST /api/v1/administrative/sync?province_code=46
GET  /api/v1/health
```

## Việc cần phát triển tiếp

- Migration Alembic và cơ chế rollback.
- CRUD cơ quan, nhóm, trạm, thành viên và ủy quyền.
- Upload/kiểm tra KML, GeoJSON; lưu geometry PostGIS.
- Overlay T1/T2, thống kê riêng rừng tự nhiên và rừng trồng.
- Sinh PDF theo thể thức văn bản hành chính và ký số.
- MFA cho SAdmin/Admin, rate limiting, object storage và virus scanning.
- Google Satellite và nhãn Google đang được nạp bằng URL tile trực tiếp, không cần API key. Đây là endpoint không được Google công bố như một API ổn định; chỉ nên dùng làm lớp nền hiển thị, không dùng làm nguồn phân tích và cần rà soát điều khoản Google trước khi vận hành chính thức.

## Lưu ý adapter 34tinhthanh.com

Schema API ngoài có thể thay đổi. Endpoint đồng bộ đã xử lý cả response dạng mảng và `{ data: [...] }`, nhưng cần chạy thử trên môi trường staging và lưu bản dữ liệu đã kiểm duyệt trước khi đưa vào báo cáo chính thức.
