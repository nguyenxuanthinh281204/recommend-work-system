# 📋 TASKS_SPRINT.MD: DANH SÁCH TASK DỰ ÁN CHO AI & DEVELOPER
> **Roadmap 4 Tuần - Chia theo Sprint - Kèm Acceptance Criteria & Checklist**

File này dùng để theo dõi tiến độ công việc. Mỗi khi bạn muốn giao việc cho AI, chỉ cần copy mã task (ví dụ: `Giao task [TASK-2.2]`) hoặc yêu cầu AI đọc file này và làm task tiếp theo.

---

## 📊 TỔNG QUAN TIẾN ĐỘ ROADMAP (4 WEEKS)

- [x] **Sprint 0: Architecture & Project Scaffolding** *(Đã hoàn thành 100%)*
- [x] **Sprint 1: Data Pipeline & Crawler (Tuần 1)** *(Đã hoàn thành 100%)*
- [ ] **Sprint 2: Entity Extraction, Normalization & Vector Database (Tuần 2)**
- [ ] **Sprint 3: CV Parsing, Hybrid Search & LLM Explainability (Tuần 3)**
- [ ] **Sprint 4: Web UI Polish, Analytics Dashboard & System Evaluation (Tuần 4)**

---

## 🏁 SPRINT 0: KHỞI TẠO NỀN TẢNG (HOÀN THÀNH ✅)
*Mục tiêu: Dựng bộ khung kiến trúc, DB pgvector, API FastAPI, Frontend React và cơ chế Dual-Mode Mock.*

- [x] **[TASK-0.1]** Thiết kế tài liệu kiến trúc tổng thể [`ARCHITECTURE.md`](file:///d:/Fresher26/mokProject2/ARCHITECTURE.md).
- [x] **[TASK-0.2]** Tạo Docker Compose (`docker-compose.yml`) cho cụm Postgres, Backend, Pipeline, Frontend.
- [x] **[TASK-0.3]** Viết schema PostgreSQL kích hoạt `pgvector`, HNSW Index, GIN Index ([`scripts/init_db.sql`](file:///d:/Fresher26/mokProject2/scripts/init_db.sql)).
- [x] **[TASK-0.4]** Khởi tạo từ điển kỹ năng chuẩn [`data/taxonomy/skills_taxonomy.json`](file:///d:/Fresher26/mokProject2/data/taxonomy/skills_taxonomy.json).
- [x] **[TASK-0.5]** Tạo Backend FastAPI với các router `/jobs`, `/match/cv`, `/analytics/hot-skills`.
- [x] **[TASK-0.6]** Cài đặt thuật toán Hybrid Search (Dense Vector + Sparse BM25 kết hợp RRF).
- [x] **[TASK-0.7]** Dựng giao diện Web Dashboard React Glassmorphism với 3 Tab chức năng.

---

## 🚀 SPRINT 1: DATA PIPELINE & CRAWLER (HOÀN THÀNH ✅)
*Mục tiêu tối thiểu: Pipeline cào và cập nhật JD hàng ngày từ nguồn công khai, tuân thủ robots.txt, lưu trữ dữ liệu sạch.*

### [TASK-1.1] Xây dựng Scrapy Spider cho tin tuyển dụng IT
- **Mô tả:** Viết spider cào dữ liệu từ 1 trang tuyển dụng IT tĩnh hoặc feed RSS công khai (ví dụ: các trang job board remote hoặc blog tuyển dụng).
- **File tác động:** [`pipelines/crawlers/it_job_spider.py`](file:///d:/Fresher26/mokProject2/pipelines/crawlers/it_job_spider.py)
- **Acceptance Criteria (Tiêu chí nghiệm thu):**
  - [x] Spider đọc file `robots.txt` của website đích trước khi cào; dừng nếu bị cấm.
  - [x] Thiết lập `DOWNLOAD_DELAY = 2.0` để không gây nghẽn/tải nặng server mục tiêu.
  - [x] Cào được tối thiểu 50-100 tin tuyển dụng thật gồm các trường: Title, Company, Location, Salary, Full Description.

### [TASK-1.2] Hoàn thiện Data Cleaning & Boilerplate Stripping
- **Mô tả:** Nâng cấp [`pipelines/processors/cleaner.py`](file:///d:/Fresher26/mokProject2/pipelines/processors/cleaner.py) để bóc tách chính xác phần Yêu cầu chuyên môn (Requirements) khỏi các thông tin phụ (Quyền lợi, Teambuilding, Giới thiệu công ty).
- **Acceptance Criteria:**
  - [x] Loại bỏ hoàn toàn mã JavaScript, CSS, thẻ HTML rác.
  - [x] Tách riêng trường `requirements_clean` sạch sẽ để phục vụ cho việc sinh Vector Embedding không bị nhiễu.

### [TASK-1.3] Thiết lập Pipeline Ingestion tự động vào PostgreSQL
- **Mô tả:** Viết script ingestion tự động kiểm tra trùng lặp (Deduplication theo URL / Title + Company) và nạp dữ liệu sạch vào bảng `jobs`.
- **File tác động:** [`pipelines/ingest_jobs.py`](file:///d:/Fresher26/mokProject2/pipelines/ingest_jobs.py)
- **Acceptance Criteria:**
  - [x] Dữ liệu mới được nạp vào PostgreSQL mà không gây lỗi khóa chính (Primary Key).
  - [x] Tự động cập nhật cột `search_vector` (`tsvector`) phục vụ tìm kiếm từ khóa.
  - [x] Tự động tính toán vector embedding và liên kết bảng `job_skills`.

---

## 🧬 SPRINT 2: ENTITY EXTRACTION & VECTOR DATABASE (TUẦN 2)
*Mục tiêu tối thiểu: Chuẩn hóa kỹ năng từ JD, mở rộng taxonomy, tạo vector embeddings hàng loạt bằng pgvector.*

### [TASK-2.1] Mở rộng bộ từ điển Taxonomy (Skill Ontology)
- **Mô tả:** Bổ sung [`data/taxonomy/skills_taxonomy.json`](file:///d:/Fresher26/mokProject2/data/taxonomy/skills_taxonomy.json) lên 150+ kỹ năng IT phổ biến tại thị trường Việt Nam & Quốc tế (phân bổ đủ: Frontend, Backend, DevOps, Data, AI, Mobile, Security, QA).
- **Acceptance Criteria:**
  - [ ] Định nghĩa đầy đủ các biến thể (Aliases) như `k8s` -> `Kubernetes`, `react.js` -> `React`, `aws cloud` -> `AWS`.

### [TASK-2.2] Tích hợp LLM Entity Extraction (JSON Mode)
- **Mô tả:** Sử dụng LLM API (OpenAI Function Calling / Structured Output) để đọc phần `requirements_clean` và trích xuất: Danh sách kỹ năng bắt buộc, Kỹ năng ưu tiên, Cấp bậc kinh nghiệm (Junior/Mid/Senior).
- **File tác động:** `pipelines/processors/llm_extractor.py`
- **Acceptance Criteria:**
  - [ ] Output trả về đúng định dạng JSON Pydantic.
  - [ ] Có cơ chế retry khi gặp rate-limit hoặc timeout.

### [TASK-2.3] Vectorization Batch Job cho toàn bộ Job Database
- **Mô tả:** Tạo script batch chạy định kỳ để embed tất cả các JD chưa có vector trong database.
- **File tác động:** `pipelines/vectorize_jobs.py`
- **Acceptance Criteria:**
  - [ ] Hỗ trợ sinh vector bằng model `text-embedding-3-small` (1536d) và fallback sang Local/Mock nếu không có internet/key.
  - [ ] Lưu vector trực tiếp vào cột `embedding` (`vector(1536)`).
  - [ ] Đảm bảo HNSW index hoạt động tối ưu.

---

## ⚡ SPRINT 3: HYBRID SEARCH & LLM REASONING (TUẦN 3)
*Mục tiêu tối thiểu: Hệ thống nhận file CV thật (PDF/DOCX), so khớp Top 10 qua Hybrid Search RRF và giải thích lý do cụ thể.*

### [TASK-3.1] Nâng cấp bộ phân tích CV (CV Parser Engine)
- **Mô tả:** Tối ưu [`backend/app/services/cv_parser.py`](file:///d:/Fresher26/mokProject2/backend/app/services/cv_parser.py) để bóc tách thông tin từ các mẫu CV PDF 2 cột, bảng biểu, icon mà không bị mất chữ.
- **Acceptance Criteria:**
  - [ ] Đọc tốt file PDF từ Canva, TopCV, Resume.io.
  - [ ] Trích xuất được email, số năm kinh nghiệm, danh sách kỹ năng cốt lõi.

### [TASK-3.2] Cân chỉnh trọng số thuật toán Hybrid Search (RRF Tuning)
- **Mô tả:** Tinh chỉnh tham số $k$ trong công thức RRF và tỷ trọng giữa Lexical BM25 (`tsvector`) và Semantic Cosine Distance (`pgvector <=>`).
- **File tác động:** `backend/app/services/hybrid_search.py`
- **Acceptance Criteria:**
  - [ ] Khi ứng viên có kỹ năng đặc thù (VD: "Kubernetes", "Golang"), các job yêu cầu đúng từ khóa này phải xuất hiện ở Top 10.
  - [ ] Khi ứng viên mô tả kinh nghiệm chung (VD: "Thiết kế kiến trúc hệ thống dữ liệu lớn"), hệ thống vẫn gợi ý được các job Data Engineer dù câu chữ không trùng 100%.

### [TASK-3.3] Nâng cấp Prompt Engineering cho phần Explainability
- **Mô tả:** Tinh chỉnh prompt tại [`backend/app/services/explainer.py`](file:///d:/Fresher26/mokProject2/backend/app/services/explainer.py) để đưa ra lý do giải thích sâu sắc, mang tính cố vấn nghề nghiệp thực tế.
- **Acceptance Criteria:**
  - [ ] Chỉ rõ 2-3 điểm mạnh mà ứng viên khớp hoàn toàn với JD.
  - [ ] Chỉ rõ chính xác 1-2 kỹ năng còn thiếu (Skill Gaps) mà JD yêu cầu.
  - [ ] Cung cấp lời khuyên cụ thể (Actionable Advice) giúp ứng viên chuẩn bị cho buổi phỏng vấn.

---

## 🎨 SPRINT 4: WEB UI, ANALYTICS DASHBOARD & ĐÁNH GIÁ (TUẦN 4)
*Mục tiêu tối thiểu: Dashboard kỹ năng hot, giao diện mượt mà, đo lường chất lượng gợi ý, đóng gói bàn giao.*

### [TASK-4.1] Hoàn thiện Dashboard Kỹ Năng Hot (Market Trends)
- **Mô tả:** Kết nối API `/api/v1/analytics/hot-skills` với giao diện biểu đồ trực quan, cho phép lọc kỹ năng theo từng ngành (DevOps, Data, AI, Backend, Frontend).
- **File tác động:** `frontend/src/App.jsx`
- **Acceptance Criteria:**
  - [ ] Hiển thị Top 15 kỹ năng được tuyển dụng nhiều nhất tính từ tập dữ liệu JD thực tế.
  - [ ] Thống kê tỷ lệ phân bổ nhu cầu giữa các nhóm ngành.

### [TASK-4.2] Tối ưu hóa UI/UX & Responsive Web
- **Mô tả:** Tinh chỉnh trải nghiệm người dùng trên mobile/tablet, thêm tính năng tải lên CV bằng cách kéo-thả (Drag & Drop) file PDF trực tiếp.
- **Acceptance Criteria:**
  - [ ] Hiển thị thông báo Toast / Loading spinner sinh động trong lúc chờ thuật toán AI tính toán.
  - [ ] Responsive hoàn hảo trên màn hình từ 375px đến 1920px.

### [TASK-4.3] Đánh giá chất lượng gợi ý (Evaluation & Benchmarking)
- **Mô tả:** Viết script benchmark đo lường chất lượng gợi ý dựa trên tập test gồm 10 CV mẫu đã được gán nhãn thủ công (Ground Truth).
- **File tác động:** `pipelines/evaluate_metrics.py`
- **Acceptance Criteria:**
  - [ ] Tính toán chỉ số **Precision@10** (Tỷ lệ job phù hợp trong top 10).
  - [ ] Tính toán chỉ số **MRR (Mean Reciprocal Rank)**.
  - [ ] So sánh hiệu quả giữa: Chỉ dùng Keyword BM25 vs Chỉ dùng Vector vs **Hybrid Search RRF**.

### [TASK-4.4] Đóng gói Docker & Tài liệu báo cáo hoàn chỉnh
- **Mô tả:** Kiểm tra toàn bộ `docker compose up -d` trên môi trường sạch, quay video demo hoặc chụp ảnh minh chứng hoạt động.
- **Acceptance Criteria:**
  - [ ] Hệ thống khởi chạy mượt mà trên bất kỳ máy nào có cài Docker chỉ bằng 1 câu lệnh.
  - [ ] README và tài liệu nghiệm thu sẵn sàng bàn giao.
