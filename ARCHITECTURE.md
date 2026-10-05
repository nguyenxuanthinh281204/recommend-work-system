# AI-Powered Job Matching & Semantic Search System (CV ↔ JD)

Hệ thống gợi ý việc làm thông minh dựa trên kỹ thuật **Hybrid Search (Dense Vector + Sparse Keyword)** và **LLM Explainability**, kết hợp Data Engineering Pipeline thu thập, làm sạch và chuẩn hóa dữ liệu tuyển dụng IT.

---

## 🏗️ 1. Kiến Trúc Tổng Thể (System Architecture)

```mermaid
flowchart TD
    subgraph Data_Source ["🌐 Data Sources & Crawler"]
        A1["IT Job Portals / Career Sites"] -->|Scrapy / Playwright| B1["Raw HTML / JSON Jobs"]
        B1 --> B2["Cleaner & Boilerplate Stripper"]
        B2 --> B3["Entity Extractor & Normalizer\n(Regex + LLM JSON Mode)"]
        B3 --> B4["Skill Taxonomy Mapping\n(ReactJS -> React, etc.)"]
    end

    subgraph Storage_Layer ["💾 Storage & Vector Layer (PostgreSQL + pgvector)"]
        B4 --> C1[("PostgreSQL DB")]
        C1 --> C2["Jobs & Structured Metadata"]
        C1 --> C3["GIN Index (tsvector - BM25 Lexical)"]
        C1 --> C4["HNSW Index (pgvector - Dense Vector)"]
        C1 --> C5["Skills & Taxonomy Master"]
    end

    subgraph Retrieval_Engine ["⚡ Hybrid Search & Ranking Engine"]
        D1["Candidate CV Upload (PDF/DOCX)"] --> D2["CV Parser & Skill Extractor"]
        D2 --> D3["Candidate Profile / Embeddings"]
        
        D3 -->|Sparse Keyword Query| C3
        D3 -->|Dense Vector Query| C4
        
        C3 -->|Top 50 Lexical| E1["Reciprocal Rank Fusion\n(RRF Algorithm)"]
        C4 -->|Top 50 Semantic| E1
        
        E1 --> E2["Candidate Pool Top 20"]
    end

    subgraph Reasoning_Layer ["🧠 LLM Reasoning & Explainability"]
        E2 --> F1["Prompt Engine (Match Explanation)"]
        F1 -->|Structured Output| F2["Score Breakdown &\nGap Analysis\n(Strengths, Missing Skills, Tips)"]
        F2 --> F3["Top 10 Ranked Jobs"]
    end

    subgraph Presentation_Layer ["🖥️ Web UI & Analytics Dashboard"]
        F3 --> G1["CV Matching View (Top 10 Cards)"]
        C1 --> G2["Skill Trends & Market Radar"]
        C1 --> G3["Job Explorer & Semantic Search"]
    end
```

---

## 🧩 2. Các Thành Phần Cốt Lõi (Core Components)

### 2.1. Data Engineering Pipeline (`/pipelines`)
* **Crawler:** Thu thập tin tuyển dụng từ các nguồn công khai, tuân thủ `robots.txt`.
* **Cleaner:** Lọc bỏ nội dung quảng cáo, phúc lợi chung chung, chỉ giữ lại phần **Job Title**, **Requirements**, **Tech Stack**, và **Level**.
* **Skill Normalizer:** Sử dụng từ điển kỹ năng chuẩn (`skills_taxonomy.json`) kết hợp trích xuất thực thể để đồng nhất hóa (ví dụ: `React.js`, `ReactJS` $\to$ `React`; `AWS Cloud` $\to$ `AWS`).

### 2.2. Storage & Vector Database (`PostgreSQL + pgvector`)
* **Kiến trúc "All-in-One":** Không cần triển khai riêng Milvus hay ElasticSearch.
* **Lexical Search:** Cột `search_vector` (`tsvector`) kết hợp `to_tsquery` để bắt chính xác các keyword bắt buộc (Java, Go, Kubernetes).
* **Dense Semantic Search:** Cột `embedding` (`vector(1536)` hoặc `vector(384)`) sử dụng thuật toán index **HNSW** cho tốc độ tìm kiếm siêu nhanh dưới 10ms.

### 2.3. Hybrid Search & RRF (`backend/app/services/hybrid_search.py`)
* Thuật toán **Reciprocal Rank Fusion (RRF)**:
  $$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + rank_m(d)}$$
  *(với $k = 60$, kết hợp thứ hạng từ Keyword Search và Dense Cosine Distance)*
* Giải quyết triệt để vấn đề:
  * Semantic Search hiểu được ngữ cảnh nhưng hay bỏ sót các từ khóa công nghệ chính xác.
  * Keyword Search tìm đúng từ khóa nhưng không hiểu được kinh nghiệm tương đương (VD: "GCP" tương đương "Cloud Platform").

### 2.4. Prompt Engineering & Reasoning (`backend/app/services/explainer.py`)
* Không chỉ trả về điểm số phần trăm đơn thuần. LLM phân tích theo 4 chiều:
  1. **Match Score (%):** Độ tương thích tổng thể.
  2. **Matched Strengths:** Những điểm mạnh ứng viên đáp ứng đúng yêu cầu tuyển dụng.
  3. **Skill Gaps:** Những công nghệ còn thiếu theo yêu cầu của JD.
  4. **Actionable Roadmap:** Lộ trình ngắn gọn để ứng viên tự học bổ sung trước khi nộp đơn.

---

## 🚀 3. Hướng Dẫn Khởi Chạy Nhanh (Quick Start)

### Yêu cầu tiên quyết
* Đã cài đặt Docker & Docker Compose.
* Tạo file cấu hình môi trường từ mẫu:
  ```bash
  cp .env.example .env
  ```

### Khởi chạy toàn bộ hệ thống
```bash
docker compose up -d --build
```

* **Backend API Documentation:** `http://localhost:8000/docs`
* **Frontend Web Dashboard:** `http://localhost:3000`
* **PostgreSQL pgvector:** `localhost:5432` (user: `postgres`, db: `jobmatch_db`)
