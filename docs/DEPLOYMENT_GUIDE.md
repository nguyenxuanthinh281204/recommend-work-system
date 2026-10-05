# 🚀 HƯỚNG DẪN TRIỂN KHAI & VẬN HÀNH (DEPLOYMENT & OPS GUIDE)

> **Mục tiêu:** Hướng dẫn kỹ sư DevOps / Developers cách triển khai, cấu hình và xử lý sự cố (Troubleshooting) toàn bộ hệ thống **MatchAI Pro**.

---

## 1. YÊU CẦU PHẦN CỨNG & HỆ ĐIỀU HÀNH
* **Hệ điều hành:** Linux (Ubuntu 22.04+), macOS, hoặc Windows 10/11 (chạy Docker Desktop với WSL2).
* **RAM:** Tối thiểu 4GB (Khuyên dùng: 8GB - 16GB).
* **Disk:** Tối thiểu 10GB dung lượng trống cho Docker images và cơ sở dữ liệu vector.
* **Phần mềm:** Docker Engine >= 24.0, Docker Compose >= 2.20.

---

## 2. QUY TRÌNH TRIỂN KHAI VỚI DOCKER COMPOSE

### Bước 1: Chuẩn bị biến môi trường
Tạo file `.env` từ file mẫu:
```bash
cp .env.example .env
```
Chỉnh sửa cấu hình nếu cần (mặc định đã cấu hình chạy chế độ `mock` để test offline).

### Bước 2: Build & Khởi động toàn bộ container
```bash
docker compose up -d --build
```

### Bước 3: Kiểm tra trạng thái các container
```bash
docker compose ps
```
Đảm bảo 4 container đều ở trạng thái `running / healthy`:
* `jobmatch_postgres` (PostgreSQL 16 + pgvector)
* `jobmatch_backend` (FastAPI)
* `jobmatch_pipeline` (ETL Seeder)
* `jobmatch_frontend` (React Web)

---

## 3. SAO LƯU & KHÔI PHỤC CƠ SỞ DỮ LIỆU (BACKUP & RESTORE)

### 📤 Sao lưu toàn bộ Database & Vectors:
```bash
docker exec -t jobmatch_postgres pg_dump -U postgres -d jobmatch_db -F c -b -v -f /tmp/backup_jobmatch.dump
docker cp jobmatch_postgres:/tmp/backup_jobmatch.dump ./backup_jobmatch.dump
```

### 📥 Khôi phục dữ liệu:
```bash
docker cp ./backup_jobmatch.dump jobmatch_postgres:/tmp/backup_jobmatch.dump
docker exec -t jobmatch_postgres pg_restore -U postgres -d jobmatch_db -v /tmp/backup_jobmatch.dump
```

---

## 4. XỬ LÝ SỰ CỐ THƯỜNG GẶP (TROUBLESHOOTING)

### ❓ 1. Lỗi cổng bị chiếm dụng (Port 5432 / 8000 / 3000 already in use):
* **Nguyên nhân:** Có dịch vụ PostgreSQL hoặc Web server nội bộ trên máy host đang chạy cùng cổng.
* **Cách khắc phục:** Đổi cổng trong file `.env` hoặc file `docker-compose.yml`:
  ```yaml
  ports:
    - "5433:5432" # Đổi cổng ngoài thành 5433
  ```

### ❓ 2. Container backend không kết nối được PostgreSQL:
* **Nguyên nhân:** PostgreSQL khởi động chậm hơn backend.
* **Cách khắc phục:** Hệ thống đã tích hợp `healthcheck` trên service `postgres` và cấu hình `condition: service_healthy` trên `backend` trong `docker-compose.yml`. Nếu vẫn gặp lỗi, chạy lệnh:
  ```bash
  docker compose restart backend
  ```

### ❓ 3. Muốn nạp lại dữ liệu demo mẫu:
```bash
docker compose exec backend python /app/data/../pipelines/seed_demo_data.py
```
*(hoặc chạy script `pipelines/seed_demo_data.py` trực tiếp từ container pipeline)*.
