# 🛡️ SECURITY_AND_CONVENTIONS.MD: BẢO MẬT & QUY ƯỚC ĐẶT TÊN DỰ ÁN

> **Mục tiêu:** Định nghĩa các chuẩn mực bảo mật thông tin, an toàn dữ liệu và quy ước lập trình (Coding & Naming Conventions) đồng bộ xuyên suốt toàn bộ dự án **MatchAI Pro**.

---

## 🔒 PHẦN 1: YÊU CẦU BẢO MẬT (SECURITY REQUIREMENTS)

### 1.1. Bảo Vệ Dữ Liệu Cá Nhân (PII - Personally Identifiable Information)
* **Xử lý CV ứng viên:**
  * File CV ứng viên tải lên (`.pdf`, `.docx`) chỉ được xử lý trong bộ nhớ (In-Memory buffer) qua `pypdf` / `python-docx`.
  * **Tuyệt đối không lưu file CV thô lên ổ cứng công khai** hoặc commit lên Git repo.
  * Chỉ trích xuất các thông tin cần thiết phục vụ so khớp: Số năm kinh nghiệm, Kỹ năng chuyên môn, Tóm tắt năng lực.
  * Địa chỉ email, số điện thoại, link cá nhân phải được hash hoặc không được hiển thị công khai ở các API public.

### 1.2. Đạo Đức & Pháp Lý Cào Dữ Liệu (Scraping Ethics & Legal)
* **Tôn trọng `robots.txt`:** Mọi crawler trước khi chạy đều phải tải và kiểm tra luật `robots.txt` của website đích.
* **Định danh User-Agent:** Phải khai báo User-Agent minh bạch (ví dụ: `User-Agent: JobMatchBot/1.0 (+http://your-domain.com/bot-info)`).
* **Kiểm soát tần suất (Rate Limiting):**
  * Bắt buộc có khoảng nghỉ tối thiểu `DOWNLOAD_DELAY = 2.0` giây giữa các lượt request.
  * Không bao giờ tấn công làm tê liệt (DoS) server nguồn.
  * Tuyệt đối không sử dụng các thủ thuật phá hoại CAPTCHA hoặc xâm nhập khu vực yêu cầu đăng nhập trái phép.

### 1.3. An Toàn Cơ Sở Dữ Liệu & Chống Injection (SQL & Vector Injection)
* **Sử dụng Parameterized Queries 100%:**
  * Toàn bộ truy vấn vào PostgreSQL + pgvector phải dùng SQLAlchemy ORM hoặc parameterized binding:
    ```python
    # CHUẨN AN TOÀN:
    db.execute(text("SELECT * FROM jobs WHERE embedding <=> :vec::vector LIMIT 10"), {"vec": vector_str})

    # CẤM TUYỆT ĐỐI (Dễ bị SQL Injection):
    db.execute(f"SELECT * FROM jobs WHERE embedding <=> '{vector_str}'::vector LIMIT 10")
    ```
* **Input Sanitization:** Mọi input từ người dùng (text tìm kiếm, text CV) phải được sanitize, loại bỏ các ký tự điều khiển nguy hiểm trước khi đưa vào hàm tính toán Full-Text Search `to_tsquery`.

### 1.4. Quản Lý Secrets & Biến Môi Trường (Zero-Secret Policy)
* **Quy tắc tuyệt đối:** Không bao giờ push API Key (OpenAI, Gemini, v.v.), mật khẩu Database, hoặc secret token vào Git.
* Mọi cấu hình phải đặt trong file `.env` (đã được cấu hình trong `.gitignore`).
* Sử dụng `pydantic-settings` ([`backend/app/core/config.py`](file:///d:/Fresher26/mokProject2/backend/app/core/config.py)) để validate kiểu dữ liệu của biến môi trường ngay khi ứng dụng khởi động.

### 1.5. Bảo Mật API & Network
* **CORS (Cross-Origin Resource Sharing):** Chỉ whitelist domain của Frontend khi triển khai Production, không dùng wildcard `*`.
* **Rate Limiting API:** Endpoint `/api/v1/match/cv` tiêu tốn tài nguyên tính toán (Vector + LLM Reasoning) nên cần giới hạn tối đa 10 requests / phút / IP để chống spam/lạm dụng.

---

## 🏷️ PHẦN 2: QUY ƯỚC ĐẶT TÊN (NAMING CONVENTIONS)

### 2.1. Cấu Trúc Thư Mục & Tệp Tin (Files & Folders)
* **Thư mục (Directories):** Luôn dùng chữ thường, phân cách bằng dấu gạch ngang hoặc gạch dưới: `app/services/`, `data/taxonomy/`.
* **Tệp tin Python:** Luôn dùng `snake_case.py` (ví dụ: `hybrid_search.py`, `cv_parser.py`, `base_crawler.py`).
* **Tệp tin React Component:** Dùng `PascalCase.jsx` (ví dụ: `JobCard.jsx`, `RadarChart.jsx`).
* **Tệp tin Tài liệu:** Dùng chữ hoa kèm gạch dưới `UPPER_SNAKE_CASE.md` (ví dụ: `README.md`, `ARCHITECTURE.md`, `TASKS_SPRINT.md`).

---

### 2.2. Quy Ước Lập Trình Backend (Python / FastAPI)
Tuân thủ tiêu chuẩn **PEP 8**:

| Thành phần | Quy ước | Ví dụ |
| :--- | :--- | :--- |
| **Modules / Files** | `snake_case` | `cv_parser.py`, `database.py` |
| **Classes / Models** | `PascalCase` | `Job`, `Skill`, `HybridSearchService`, `JobResponse` |
| **Functions / Methods** | `snake_case` | `get_embedding()`, `search()`, `explain_match()` |
| **Variables / Arguments** | `snake_case` | `query_vector`, `match_score`, `job_id` |
| **Constants / Configs** | `UPPER_SNAKE_CASE` | `API_V1_STR`, `EMBEDDING_DIM`, `TAXONOMY_PATH` |
| **Pydantic Schemas** | Danh từ + suffix | `JobCreate`, `JobResponse`, `CVMatchResponse` |

---

### 2.3. Quy Ước Cơ Sở Dữ Liệu (PostgreSQL & pgvector)

| Thành phần | Quy ước | Ví dụ |
| :--- | :--- | :--- |
| **Tên bảng (Tables)** | `snake_case` ở dạng **số nhiều** | `jobs`, `skills`, `job_skills` |
| **Cột khóa chính (PK)** | Luôn đặt tên là `id` | `id SERIAL PRIMARY KEY` |
| **Cột khóa ngoại (FK)** | `<singular_table>_id` | `job_id`, `skill_id` |
| **Cột vector** | Luôn đặt tên là `embedding` | `embedding vector(1536)` |
| **Cột tìm kiếm từ khóa**| Luôn đặt tên là `search_vector` | `search_vector tsvector` |
| **Chỉ mục (Indexes)** | `idx_<table>_<column>_<type>` | `idx_jobs_search_vector`, `idx_jobs_embedding_hnsw` |
| **Thời gian (Timestamps)** | `created_at`, `updated_at` | `TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP` |

---

### 2.4. Quy Ước Lập Trình Frontend (React / JavaScript / CSS)

| Thành phần | Quy ước | Ví dụ |
| :--- | :--- | :--- |
| **React Components** | `PascalCase` | `App.jsx`, `JobCard.jsx`, `MatchBadge.jsx` |
| **Custom Hooks** | `useCamelCase` | `useJobSearch.js`, `useDebounce.js` |
| **Helper Functions** | `camelCase` | `formatSalary()`, `calculateScoreColor()` |
| **CSS Variables** | `--kebab-case` | `--bg-dark`, `--primary-glow`, `--accent-cyan` |
| **CSS Class Names** | `kebab-case` ngữ nghĩa | `.glass-panel`, `.score-badge`, `.skill-tag` |

---

### 2.5. Quy Ước Git (Git Branch & Commit Messages)
Tuân thủ chuẩn **Conventional Commits**:

* **Quy tắc đặt tên Branch:**
  * Tính năng mới: `feature/cv-parser-pdf`, `feature/hybrid-search-rrf`
  * Sửa lỗi: `fix/pgvector-connection-timeout`, `fix/ui-mobile-overflow`
  * Tài liệu: `docs/architecture-update`

* **Quy tắc đặt tên Commit Message:**
  * `feat:` Tính năng mới (ví dụ: `feat: implement RRF hybrid ranking algorithm`)
  * `fix:` Sửa lỗi (ví dụ: `fix: handle empty candidate skills gracefully`)
  * `docs:` Cập nhật tài liệu (ví dụ: `docs: add security guidelines and conventions`)
  * `refactor:` Tối ưu hóa code mà không thay đổi logic chức năng
  * `perf:` Cải thiện hiệu năng (ví dụ: `perf: add HNSW index for sub-10ms vector retrieval`)
  * `test:` Thêm hoặc sửa unit test
