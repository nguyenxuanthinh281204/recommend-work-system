import os
import sys
import time
import hashlib
import numpy as np
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Ensure path includes workspace root
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir.parent))

from pipelines.crawlers.it_job_spider import it_job_spider
from pipelines.processors.cleaner import job_cleaner
from pipelines.processors.normalizer import skill_normalizer

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/jobmatch_db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "mock-key")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "mock")

def generate_embedding(text_content: str, dim: int = 1536) -> list:
    """Dual-mode embedding generator: OpenAI if key provided, else deterministic mock."""
    if EMBEDDING_PROVIDER == "openai" and OPENAI_API_KEY != "mock-key":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            res = client.embeddings.create(
                input=[text_content[:2000]],
                model="text-embedding-3-small"
            )
            return res.data[0].embedding
        except Exception as e:
            print(f"[WARN] OpenAI embedding failed ({e}), using mock.")

    # Deterministic Mock Vector
    words = [w.lower().strip() for w in text_content.split() if len(w) > 1]
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

def run_ingestion_pipeline(limit: int = 50):
    start_time = time.time()
    print("=" * 60)
    print("🚀 STARTING IT JOB INGESTION PIPELINE (DE & AI)")
    print("=" * 60)

    # 1. Connect to PostgreSQL
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        # Test connection
        db.execute(text("SELECT 1"))
        print("[DB] Successfully connected to PostgreSQL + pgvector.")
    except Exception as e:
        print(f"[ERROR] Cannot connect to Database at {DATABASE_URL}: {e}")
        print("[TIP] Ensure PostgreSQL is running via `docker compose up -d postgres`.")
        return

    try:
        # Load skill dictionary mapping
        skills_rows = db.execute(text("SELECT id, name FROM skills")).fetchall()
        skill_id_map = {row.name: row.id for row in skills_rows}
        print(f"[DB] Loaded {len(skill_id_map)} canonical skills from taxonomy.")

        # 2. Crawl and parse jobs
        raw_jobs = it_job_spider.crawl_public_tech_feed(limit=limit)
        
        inserted_count = 0
        skipped_count = 0
        skills_associated_count = 0

        for job in raw_jobs:
            title = job["title"]
            company = job["company"]
            url = job["source_url"]

            # Deduplication: Check if job already exists by URL or (Title + Company)
            existing = db.execute(text("""
                SELECT id FROM jobs 
                WHERE source_url = :url OR (title = :title AND company = :company)
            """), {"url": url, "title": title, "company": company}).fetchone()

            if existing:
                skipped_count += 1
                continue

            # 3. Generate Vector Embedding
            embed_text = f"{title}. Requirements: {job['requirements_clean']}"
            embedding = generate_embedding(embed_text)
            vec_str = "[" + ",".join(map(str, embedding)) + "]"

            # 4. Insert into PostgreSQL
            insert_sql = text("""
                INSERT INTO jobs (
                    title, company, location, salary_range, 
                    experience_level, job_type, description_raw, 
                    requirements_clean, source_url, embedding
                ) VALUES (
                    :title, :company, :location, :salary_range,
                    :experience_level, :job_type, :description_raw,
                    :requirements_clean, :source_url, :embedding::vector
                ) RETURNING id
            """)
            res = db.execute(insert_sql, {
                "title": title,
                "company": company,
                "location": job["location"],
                "salary_range": job["salary_range"],
                "experience_level": job["experience_level"],
                "job_type": job["job_type"],
                "description_raw": job["description_raw"],
                "requirements_clean": job["requirements_clean"],
                "source_url": url,
                "embedding": vec_str
            })
            job_id = res.fetchone()[0]
            inserted_count += 1

            # 5. Associate Normalized Skills
            for skill_name in job["skills"]:
                if skill_name in skill_id_map:
                    sid = skill_id_map[skill_name]
                    db.execute(text("""
                        INSERT INTO job_skills (job_id, skill_id, is_required)
                        VALUES (:jid, :sid, TRUE)
                        ON CONFLICT DO NOTHING
                    """), {"jid": job_id, "sid": sid})
                    skills_associated_count += 1

        db.commit()

        elapsed = round(time.time() - start_time, 2)
        total_in_db = db.execute(text("SELECT COUNT(*) FROM jobs")).scalar()

        print("\n" + "=" * 60)
        print("✅ INGESTION PIPELINE SUMMARY:")
        print(f"• Total Processed from Feed: {len(raw_jobs)}")
        print(f"• Newly Inserted into DB:    {inserted_count}")
        print(f"• Skipped Duplicates:        {skipped_count}")
        print(f"• Skill Relations Mapped:    {skills_associated_count}")
        print(f"• Total Active Jobs in DB:   {total_in_db}")
        print(f"• Execution Time:            {elapsed}s")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Pipeline execution failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    limit_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    run_ingestion_pipeline(limit=limit_arg)
