# 🚀 MatchAI Pro: Intelligent Semantic CV-JD Matching System
> **Hybrid Search (Dense Vector + Sparse BM25) & LLM Explainability**

Hệ thống gợi ý việc làm thông minh kết hợp **Data Engineering** (Crawl, Clean, Entity Normalization) và **AI Engineering** (Semantic Search pgvector, RRF Ranking, LLM Reasoning).

---

## 🏛️ 1. Architecture Overview (Kiến Trúc Tổng Thể)

```
[Candidate CV (PDF/Text)]                 [Public IT Job Portals]
          │                                         │
          ▼ (pypdf/docx)                            ▼ (Scrapy/Playwright)
  [CV Text Parser]                          [HTML Cleaner & Stripper]
          │                                         │
          ▼                                         ▼
[Skill Entity Extraction] ──(Taxonomy Mapping)──► [Skill Normalizer]
          │                                         │
          ├─────────────────────┐                   ▼
          ▼                     ▼          [PostgreSQL 16 + pgvector]
[Candidate Embedding]    [Skill Tokens]         ├── Jobs (Metadata)
          │                     │               ├── HNSW Vector Index (Dense)
          │ (Dense Cosine)      │ (Sparse BM25) └── GIN tsvector Index (Lexical)
          └───────────┬─────────┘
                      ▼
       [Reciprocal Rank Fusion (RRF)]
                      ▼
         [Candidate Pool Top 20]
                      ▼
     [LLM Reasoning & Explainability]
   (Score, Strengths, Skill Gaps, Advice)
                      ▼
          [Top 10 Matched Jobs UI]
```

---

## 🛠️ 2. Tech Stack Chi Tiết

| Thành phần | Công nghệ sử dụng | Vai trò & Lý do lựa chọn |
| :--- | :--- | :--- |
| **Database & Vector Engine** | **PostgreSQL 16 + pgvector** | Đóng vai trò **"All-in-One DB"**: vừa lưu Relational, vừa Full-Text Search (BM25 `tsvector`), vừa Vector Search (HNSW Index Cosine `<=>`). Không cần dựng riêng Milvus/Elasticsearch. |
| **Backend API** | **FastAPI (Python 3.11)** | Hiệu năng cao, async I/O, OpenAPI Swagger tự động, Pydantic type validation. |
| **Orchestration / ETL** | **Python Pipeline / Scrapy** | Thu thập tin tuyển dụng, làm sạch boilerplate, chuẩn hóa kỹ năng qua từ điển taxonomy. |
| **Embedding Model** | **text-embedding-3-small / BGE** | Vector hóa ngữ cảnh yêu cầu công việc (1536 chiều), hỗ trợ cả Mock offline mode. |
| **LLM Reasoning** | **GPT-4o-mini / Pydantic JSON** | Phân tích giải thích lý do khớp (Matched Strengths, Missing Gaps, Career Advice). |
| **Frontend UI** | **React + Vite + Modern CSS** | Giao diện Dark Cyberpunk, Glassmorphism, hiển thị kết quả trực quan kèm biểu đồ kỹ năng hot. |
| **DevOps** | **Docker & Docker Compose** | Đóng gói toàn bộ cụm dịch vụ trong 1 lệnh duy nhất. |

---

## 📁 3. Cấu Trúc Thư Mục (Directory Structure)

```bash
mokProject2/
├── docker-compose.yml              # Orchestration toàn bộ hệ thống
├── .env.example                     # File biến môi trường mẫu
├── ARCHITECTURE.md                  # Tài liệu phân tích kiến trúc chi tiết
├── scripts/
│   └── init_db.sql                 # Script khởi tạo pgvector, bảng và index
├── data/
│   └── taxonomy/
│       └── skills_taxonomy.json    # Từ điển chuẩn hóa kỹ năng IT
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py                 # FastAPI App & CORS setup
│       ├── core/                   # Cấu hình DB & Settings
│       ├── models/                 # SQLAlchemy models (Job, Skill, pgvector)
│       ├── schemas/                # Pydantic schemas
│       ├── services/
│       │   ├── embedding.py        # Service sinh embedding (OpenAI + Mock)
│       │   ├── cv_parser.py        # Bóc tách CV PDF/Word & Entity
│       │   ├── hybrid_search.py    # Thuật toán Hybrid Search & RRF
│       │   └── explainer.py        # Prompt Engineering sinh lý do gợi ý
│       └── api/v1/                 # Endpoints (jobs, match, analytics)
├── pipelines/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── crawlers/                   # Module cào dữ liệu tuyển dụng
│   ├── processors/                 # Làm sạch HTML và chuẩn hóa skills
│   └── seed_demo_data.py           # Script nạp 10+ JD mẫu kèm vector có sẵn
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx                 # UI Tabs: CV Matcher, Analytics Radar, Explorer
        └── index.css               # Design system Glassmorphism & Animations
```

---

## 🚀 4. Hướng Dẫn Khởi Chạy (Quick Start)

### Cách 1: Khởi chạy bằng Docker Compose (Khuyên dùng)

1. Sao chép file môi trường:
   ```bash
   cp .env.example .env
   ```

2. Khởi chạy toàn bộ hệ thống bằng 1 lệnh:
   ```bash
   docker compose up -d --build
   ```

3. Truy cập ứng dụng:
   - **Frontend Web Dashboard:** [http://localhost:3000](http://localhost:3000)
   - **Backend Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Healthcheck:** [http://localhost:8000/health](http://localhost:8000/health)

---

### Cách 2: Chạy kiểm thử cục bộ (Local Development)

#### Frontend (Node 18+):
```bash
cd frontend
npm install
npm run dev
```

---

## 📚 5. Thư Mục Tài Liệu Kỹ Thuật (Documentation Hub)

Toàn bộ tài liệu chuyên sâu được lưu trữ có hệ thống tại thư mục [`docs/`](file:///d:/Fresher26/mokProject2/docs/README.md):

* 📡 **API Specification:** [`docs/API_SPECIFICATION.md`](file:///d:/Fresher26/mokProject2/docs/API_SPECIFICATION.md)
* 🧠 **Hybrid Search & RRF Algorithm:** [`docs/HYBRID_SEARCH_ALGORITHM.md`](file:///d:/Fresher26/mokProject2/docs/HYBRID_SEARCH_ALGORITHM.md)
* 💾 **Database Schema & Indexes:** [`docs/DATABASE_SCHEMA.md`](file:///d:/Fresher26/mokProject2/docs/DATABASE_SCHEMA.md)
* 🚀 **Deployment & Ops Guide:** [`docs/DEPLOYMENT_GUIDE.md`](file:///d:/Fresher26/mokProject2/docs/DEPLOYMENT_GUIDE.md)
* 🛡️ **Security & Naming Conventions:** [`SECURITY_AND_CONVENTIONS.md`](file:///d:/Fresher26/mokProject2/SECURITY_AND_CONVENTIONS.md)
* 🎯 **Features & Use Cases:** [`FEATURES_AND_USE_CASES.md`](file:///d:/Fresher26/mokProject2/FEATURES_AND_USE_CASES.md)
* 📋 **Sprint Tasks Roadmap:** [`TASKS_SPRINT.md`](file:///d:/Fresher26/mokProject2/TASKS_SPRINT.md)
* 🤖 **AI Assistant Contract:** [`AGENTS.md`](file:///d:/Fresher26/mokProject2/AGENTS.md)

