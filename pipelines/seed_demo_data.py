import os
import hashlib
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/jobmatch_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generate_mock_embedding(text: str, dim: int = 1536):
    words = [w.lower().strip() for w in text.split() if len(w) > 1]
    vec = np.zeros(dim, dtype=np.float32)
    for word in words:
        h = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if (h % 2 == 0) else -1.0
        vec[idx] += sign
        idx2 = (h // dim) % dim
        vec[idx2] += 0.5 * sign
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    else:
        vec[0] = 1.0
    return vec.tolist()

DEMO_JOBS = [
    {
        "title": "Senior DevOps & Cloud Engineer",
        "company": "CloudNative Tech Global",
        "location": "Remote / Ho Chi Minh",
        "salary_range": "$2,500 - $3,500",
        "experience_level": "Senior",
        "job_type": "Full-time",
        "requirements_clean": "Proficient in Docker, Kubernetes orchestration, Helm. Strong hands-on experience with AWS (EKS, EC2, S3, IAM) and Terraform. Expertise in CI/CD pipeline automation (GitHub Actions, GitLab CI). Experience with Prometheus, Grafana, and Linux administration.",
        "skills": ["Docker", "Kubernetes", "AWS", "CI/CD"]
    },
    {
        "title": "Senior Data Engineer (Airflow & Spark)",
        "company": "Fintech Analytics Ltd",
        "location": "Hanoi / Hybrid",
        "salary_range": "$2,200 - $3,200",
        "experience_level": "Senior",
        "job_type": "Full-time",
        "requirements_clean": "Strong background in building scalable batch and streaming pipelines. Proficient in Apache Airflow, Apache Spark, and Python. Solid experience with PostgreSQL, Data Lakes, and AWS cloud services. Good knowledge of dimensional data modeling and SQL query tuning.",
        "skills": ["Apache Airflow", "Apache Spark", "Python", "PostgreSQL", "AWS"]
    },
    {
        "title": "AI / LLM Engineer (RAG & Semantic Search)",
        "company": "NextGen AI Labs",
        "location": "Remote",
        "salary_range": "$2,000 - $3,000",
        "experience_level": "Mid-Level",
        "job_type": "Full-time",
        "requirements_clean": "Hands-on experience deploying Deep Learning / LLM applications and RAG architectures. Proficient in Python, FastAPI, and Vector Search databases like pgvector, Milvus, or Pinecone. Experience with LangChain, LlamaIndex, prompt engineering, and model evaluation.",
        "skills": ["Python", "FastAPI", "Deep Learning / LLM", "Vector Search"]
    },
    {
        "title": "Fullstack Developer (React & Node.js)",
        "company": "VentureScale Studios",
        "location": "Da Nang / Hybrid",
        "salary_range": "$1,500 - $2,200",
        "experience_level": "Mid-Level",
        "job_type": "Full-time",
        "requirements_clean": "Strong experience with modern React, TypeScript, and state management. Backend expertise with Node.js, Express/NestJS, and PostgreSQL. Familiar with Docker containerization, RESTful APIs, and writing clean, testable code.",
        "skills": ["React", "TypeScript", "Node.js", "PostgreSQL", "Docker"]
    },
    {
        "title": "Backend Golang Engineer (High Concurrency)",
        "company": "HyperScale Gaming",
        "location": "Ho Chi Minh / Remote",
        "salary_range": "$2,000 - $3,000",
        "experience_level": "Senior",
        "job_type": "Full-time",
        "requirements_clean": "Expertise in Go (Golang) microservices, goroutines, and channels. Deep understanding of Redis caching, PostgreSQL transaction management, and gRPC. Experience deploying to Kubernetes clusters and building high-throughput APIs.",
        "skills": ["Go", "Docker", "Kubernetes", "Redis", "PostgreSQL"]
    },
    {
        "title": "Senior Java Spring Boot Engineer",
        "company": "Enterprise Banking Solutions",
        "location": "Hanoi",
        "salary_range": "$1,800 - $2,600",
        "experience_level": "Senior",
        "job_type": "Full-time",
        "requirements_clean": "Extensive experience with Java 11/17, Spring Boot, Spring Cloud, and Hibernate. Solid knowledge of PostgreSQL, Redis caching, and message queues (Kafka/RabbitMQ). Experience with Docker, CI/CD pipelines, and microservices architecture.",
        "skills": ["Java", "Spring Boot", "PostgreSQL", "Redis", "Docker", "CI/CD"]
    },
    {
        "title": "Junior Python Backend Developer",
        "company": "E-Commerce Growth Hub",
        "location": "Ho Chi Minh",
        "salary_range": "$800 - $1,200",
        "experience_level": "Junior",
        "job_type": "Full-time",
        "requirements_clean": "Solid foundation in Python and FastAPI or Django. Familiar with PostgreSQL relational queries and REST API principles. Basic experience with Docker containers and Git workflow. Passionate about learning new software engineering patterns.",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"]
    },
    {
        "title": "Machine Learning Engineer (Computer Vision / NLP)",
        "company": "AI Robotics Corp",
        "location": "Remote",
        "salary_range": "$1,800 - $2,800",
        "experience_level": "Mid-Level",
        "job_type": "Full-time",
        "requirements_clean": "Strong mathematical foundation in Machine Learning and Deep Learning. Proficiency in Python, PyTorch, and Scikit-Learn. Experience with model deployment using FastAPI and Docker. Knowledge of MLOps pipelines is a strong plus.",
        "skills": ["Python", "Machine Learning", "Deep Learning / LLM", "Docker"]
    }
]

def seed_database():
    print("[INFO] Connecting to database...")
    db = SessionLocal()
    try:
        # Check existing jobs
        existing_count = db.execute(text("SELECT COUNT(*) FROM jobs")).scalar()
        if existing_count and existing_count > 0:
            print(f"[INFO] Database already contains {existing_count} jobs. Checking embeddings...")
        
        # Load skill id mapping
        skills_rows = db.execute(text("SELECT id, name FROM skills")).fetchall()
        skill_id_map = {row.name: row.id for row in skills_rows}

        for item in DEMO_JOBS:
            # Check if job title already exists
            existing = db.execute(text("SELECT id FROM jobs WHERE title = :t AND company = :c"), {
                "t": item["title"],
                "c": item["company"]
            }).fetchone()

            if existing:
                job_id = existing[0]
                print(f"[SKIP] Job '{item['title']}' already exists.")
            else:
                embedding = generate_mock_embedding(item["title"] + " " + item["requirements_clean"])
                vec_str = "[" + ",".join(map(str, embedding)) + "]"
                
                insert_sql = text("""
                    INSERT INTO jobs (title, company, location, salary_range, experience_level, job_type, description_raw, requirements_clean, embedding)
                    VALUES (:title, :company, :location, :salary_range, :experience_level, :job_type, :description_raw, :requirements_clean, :embedding::vector)
                    RETURNING id
                """)
                res = db.execute(insert_sql, {
                    "title": item["title"],
                    "company": item["company"],
                    "location": item["location"],
                    "salary_range": item["salary_range"],
                    "experience_level": item["experience_level"],
                    "job_type": item["job_type"],
                    "description_raw": item["requirements_clean"],
                    "requirements_clean": item["requirements_clean"],
                    "embedding": vec_str
                })
                job_id = res.fetchone()[0]
                print(f"[INSERT] Added Job: {item['title']} (ID: {job_id})")

            # Associate skills in job_skills
            for s_name in item["skills"]:
                if s_name in skill_id_map:
                    sid = skill_id_map[s_name]
                    db.execute(text("""
                        INSERT INTO job_skills (job_id, skill_id, is_required)
                        VALUES (:jid, :sid, TRUE)
                        ON CONFLICT DO NOTHING
                    """), {"jid": job_id, "sid": sid})

        db.commit()
        print("[SUCCESS] Database seeded successfully with demo jobs and embeddings!")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to seed database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
