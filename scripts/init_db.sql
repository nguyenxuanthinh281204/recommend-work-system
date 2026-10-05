-- ==============================================================
-- Database Initialization Script for AI-Powered Job Matching System
-- PostgreSQL 16 + pgvector extension
-- ==============================================================

-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create Skills Reference Table (Taxonomy)
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    aliases TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create Jobs Table
-- Note: embedding dimension is set to 1536 (OpenAI text-embedding-3-small standard)
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(100) DEFAULT 'Remote',
    salary_range VARCHAR(100),
    experience_level VARCHAR(50) DEFAULT 'Mid-Level', -- Fresher, Junior, Mid, Senior, Lead
    job_type VARCHAR(50) DEFAULT 'Full-time',
    description_raw TEXT NOT NULL,
    requirements_clean TEXT NOT NULL,
    source_url TEXT,
    posted_date DATE DEFAULT CURRENT_DATE,
    
    -- Lexical Search (Full-Text Search BM25 support)
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(title, '') || ' ' || coalesce(requirements_clean, ''))
    ) STORED,

    -- Dense Vector Search (pgvector HNSW)
    embedding vector(1536),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create Job-Skills Junction Table
CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    is_required BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (job_id, skill_id)
);

-- 5. Indexes for Ultra-Fast Search Performance
-- Lexical GIN Index
CREATE INDEX IF NOT EXISTS idx_jobs_search_vector ON jobs USING GIN (search_vector);

-- HNSW Vector Index for Cosine Distance (<=>)
-- m=16, ef_construction=64 gives high recall (>98%) with sub-millisecond retrieval
CREATE INDEX IF NOT EXISTS idx_jobs_embedding_hnsw ON jobs 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);

-- Standard indexes for filtering
CREATE INDEX IF NOT EXISTS idx_jobs_exp_level ON jobs (experience_level);
CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs (location);

-- 6. Insert Core Skills Taxonomy
INSERT INTO skills (name, category, aliases) VALUES
('Python', 'Backend', ARRAY['python', 'python3', 'py']),
('FastAPI', 'Backend', ARRAY['fastapi', 'fast-api']),
('Java', 'Backend', ARRAY['java', 'core java', 'java 8', 'java 11', 'java 17']),
('Spring Boot', 'Backend', ARRAY['spring boot', 'springboot', 'spring-boot']),
('Node.js', 'Backend', ARRAY['nodejs', 'node.js', 'node', 'expressjs']),
('Go', 'Backend', ARRAY['golang', 'go language', 'go']),
('React', 'Frontend', ARRAY['reactjs', 'react.js', 'react', 'react 18']),
('Vue.js', 'Frontend', ARRAY['vue', 'vuejs', 'vue.js']),
('TypeScript', 'Frontend', ARRAY['typescript', 'ts']),
('Docker', 'DevOps & Cloud', ARRAY['docker', 'docker compose', 'containerization']),
('Kubernetes', 'DevOps & Cloud', ARRAY['k8s', 'kubernetes', 'kube']),
('AWS', 'DevOps & Cloud', ARRAY['aws', 'amazon web services', 'ec2', 's3', 'lambda']),
('CI/CD', 'DevOps & Cloud', ARRAY['ci/cd', 'github actions', 'gitlab ci', 'jenkins']),
('PostgreSQL', 'Database', ARRAY['postgres', 'postgresql', 'psql', 'pgvector']),
('MongoDB', 'Database', ARRAY['mongodb', 'mongo']),
('Redis', 'Database', ARRAY['redis', 'cache']),
('Apache Airflow', 'Data & AI', ARRAY['airflow', 'apache airflow', 'dagster']),
('Apache Spark', 'Data & AI', ARRAY['spark', 'pyspark']),
('Machine Learning', 'Data & AI', ARRAY['ml', 'machine learning', 'scikit-learn']),
('Deep Learning / LLM', 'Data & AI', ARRAY['llm', 'deep learning', 'pytorch', 'rag', 'langchain', 'openai']),
('Vector Search', 'Data & AI', ARRAY['vector search', 'pgvector', 'semantic search', 'embeddings'])
ON CONFLICT (name) DO NOTHING;
