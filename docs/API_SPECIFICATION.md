# 📡 TÀI LIỆU ĐẶC TẢ API (API SPECIFICATION)
> **Base URL:** `http://localhost:8000/api/v1`  
> **Interactive Swagger UI:** `http://localhost:8000/docs`  
> **OpenAPI JSON:** `http://localhost:8000/api/v1/openapi.json`

---

## 1. HỆ THỐNG GỢI Ý & SO KHỚP CV (MATCHING API)

### 📌 Endpoint: `POST /match/cv`
Nhận CV của ứng viên (dưới dạng file tải lên hoặc đoạn văn bản thô), thực hiện trích xuất thực thể, truy vấn Hybrid Search và gọi LLM Reasoning để trả về Top 10 việc làm phù hợp nhất kèm giải thích chi tiết.

* **Content-Type:** `multipart/form-data`
* **Request Parameters:**

| Tham số | Kiểu dữ liệu | Bắt buộc | Mô tả |
| :--- | :--- | :---: | :--- |
| `file` | Binary File | Không* | File CV định dạng `.pdf`, `.docx` hoặc `.txt` |
| `cv_text` | String | Không* | Đoạn văn bản CV dán trực tiếp |
| `top_k` | Integer | Không | Số lượng công việc tối đa muốn trả về (Mặc định: `10`) |

*\* Lưu ý: Bắt buộc phải có ít nhất 1 trong 2 trường `file` hoặc `cv_text`.*

#### 📤 Request Ví dụ (cURL):
```bash
curl -X POST "http://localhost:8000/api/v1/match/cv" \
  -F "cv_text=Nguyễn Văn A - 3 years experience in Docker, Kubernetes, AWS, CI/CD pipelines." \
  -F "top_k=5"
```

#### 📥 Response Ví dụ (200 OK):
```json
{
  "candidate": {
    "name": "Nguyễn Văn A",
    "email": null,
    "years_of_experience": 3.0,
    "detected_skills": ["Docker", "Kubernetes", "AWS", "CI/CD"],
    "summary": "Nguyễn Văn A - 3 years experience in Docker, Kubernetes, AWS, CI/CD pipelines."
  },
  "top_matches": [
    {
      "job": {
        "id": 1,
        "title": "Senior DevOps & Cloud Engineer",
        "company": "CloudNative Tech Global",
        "location": "Remote / Ho Chi Minh",
        "salary_range": "$2,500 - $3,500",
        "experience_level": "Senior",
        "job_type": "Full-time",
        "requirements_clean": "Proficient in Docker, Kubernetes orchestration, Helm. Strong hands-on experience with AWS...",
        "skills": [
          {"id": 10, "name": "Docker", "category": "DevOps & Cloud"},
          {"id": 11, "name": "Kubernetes", "category": "DevOps & Cloud"},
          {"id": 12, "name": "AWS", "category": "DevOps & Cloud"},
          {"id": 13, "name": "CI/CD", "category": "DevOps & Cloud"}
        ]
      },
      "match_score": 92,
      "matched_skills": ["Docker", "Kubernetes", "AWS", "CI/CD"],
      "missing_skills": [],
      "reasoning": {
        "match_score": 92,
        "matched_strengths": [
          "Strong foundation in Docker, Kubernetes aligns directly with Senior DevOps expectations.",
          "AWS hands-on cloud experience matches infrastructure requirements."
        ],
        "skill_gaps": [
          "Ensure experience with Terraform / IaC is highlighted during the interview."
        ],
        "career_advice": "Profile is well-aligned with position requirements. Focus on production incident management experience."
      }
    }
  ],
  "total_evaluated": 1
}
```

---

## 2. QUẢN LÝ & TÌM KIẾM VIỆC LÀM (JOBS API)

### 📌 Endpoint: `GET /jobs`
Lấy danh sách các tin tuyển dụng đang có trong hệ thống, hỗ trợ phân trang và lọc theo cấp bậc kinh nghiệm.

* **Query Parameters:**
  * `skip` (int, default: 0): Số bản ghi bỏ qua.
  * `limit` (int, default: 20): Số bản ghi lấy tối đa.
  * `experience_level` (string, optional): Lọc theo `Junior`, `Mid-Level`, `Senior`.

#### 📤 Request Ví dụ:
```bash
curl -X GET "http://localhost:8000/api/v1/jobs?limit=5&experience_level=Senior"
```

---

### 📌 Endpoint: `GET /jobs/search`
Tìm kiếm việc làm kết hợp từ khóa ngữ nghĩa và full-text search.

* **Query Parameters:**
  * `q` (string, required): Câu truy vấn tìm kiếm (VD: `"Python FastAPI Machine Learning"`).
  * `limit` (int, default: 10): Số lượng kết quả.

#### 📥 Response Ví dụ (200 OK):
```json
[
  {
    "job": {
      "id": 3,
      "title": "AI / LLM Engineer (RAG & Semantic Search)",
      "company": "NextGen AI Labs",
      "salary_range": "$2,000 - $3,000",
      "experience_level": "Mid-Level"
    },
    "lexical_score": 0.0,
    "vector_score": 0.0,
    "combined_score": 0.0328
  }
]
```

---

## 3. THỐNG KÊ THỊ TRƯỜNG & KỸ NĂNG HOT (ANALYTICS API)

### 📌 Endpoint: `GET /analytics/hot-skills`
Thống kê các kỹ năng công nghệ có nhu cầu tuyển dụng cao nhất trên toàn bộ cơ sở dữ liệu JD.

#### 📤 Request Ví dụ:
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/hot-skills?limit=10"
```

#### 📥 Response Ví dụ (200 OK):
```json
{
  "top_skills": [
    {"skill": "Python", "category": "Backend", "count": 18},
    {"skill": "Docker", "category": "DevOps & Cloud", "count": 16},
    {"skill": "PostgreSQL", "category": "Database", "count": 15},
    {"skill": "Kubernetes", "category": "DevOps & Cloud", "count": 12},
    {"skill": "AWS", "category": "DevOps & Cloud", "count": 12}
  ],
  "categories": [
    {"category": "DevOps & Cloud", "count": 40},
    {"category": "Data & AI", "count": 34},
    {"category": "Backend", "count": 28}
  ]
}
```

---

## 4. KIỂM TRA TRẠNG THÁI HỆ THỐNG (HEALTHCHECK)

### 📌 Endpoint: `GET /health`
* **Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "AI-Powered Job Matching System",
  "embedding_provider": "mock",
  "llm_provider": "mock"
}
```
