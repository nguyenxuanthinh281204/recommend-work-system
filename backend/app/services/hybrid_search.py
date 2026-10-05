from typing import List, Tuple, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.job import Job
from app.services.embedding import embedding_service

class HybridSearchService:
    @staticmethod
    def rrf_score(rank: int, k: int = 60) -> float:
        """Calculate Reciprocal Rank Fusion score."""
        return 1.0 / (k + rank)

    @classmethod
    def search(
        cls,
        db: Session,
        query_text: str,
        query_skills: List[str] = None,
        top_k: int = 20,
        rrf_k: int = 60
    ) -> List[Tuple[Job, float]]:
        """
        Executes Hybrid Search:
        1. Dense Vector Search via pgvector Cosine Distance (<=>)
        2. Lexical / Keyword Search via PostgreSQL tsvector full-text search
        3. Reciprocal Rank Fusion (RRF) to produce the balanced top candidate list
        """
        query_skills = query_skills or []
        
        # Step 1: Generate Embedding for query (CV summary or query text)
        query_vector = embedding_service.get_embedding(query_text)
        vector_str = "[" + ",".join(map(str, query_vector)) + "]"

        # Dense Vector Query: Retrieve top 40 candidates by Cosine Distance
        dense_sql = text("""
            SELECT id, (embedding <=> :vec::vector) AS cosine_dist
            FROM jobs
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> :vec::vector ASC
            LIMIT 40
        """)
        dense_results = db.execute(dense_sql, {"vec": vector_str}).fetchall()
        
        dense_ranks: Dict[int, int] = {}
        for rank, row in enumerate(dense_results, start=1):
            dense_ranks[row.id] = rank

        # Step 2: Lexical / Keyword Search Query: Retrieve top 40 candidates
        # Construct search query from skills or query text
        terms = [re_term.strip() for re_term in query_skills if re_term.strip()]
        if not terms:
            terms = [w.strip() for w in query_text.split()[:5] if len(w.strip()) > 2]
        
        lexical_query = " | ".join(terms) if terms else "developer"
        
        lexical_sql = text("""
            SELECT id, ts_rank(search_vector, plainto_tsquery('english', :q)) AS rank_score
            FROM jobs
            WHERE search_vector @@ plainto_tsquery('english', :q)
            ORDER BY rank_score DESC
            LIMIT 40
        """)
        try:
            lexical_results = db.execute(lexical_sql, {"q": lexical_query}).fetchall()
        except Exception:
            lexical_results = []

        lexical_ranks: Dict[int, int] = {}
        for rank, row in enumerate(lexical_results, start=1):
            lexical_ranks[row.id] = rank

        # Step 3: Reciprocal Rank Fusion (RRF)
        all_job_ids = set(dense_ranks.keys()).union(set(lexical_ranks.keys()))
        
        # If both are empty (e.g., initial empty db or no matches), fallback to latest jobs
        if not all_job_ids:
            fallback_jobs = db.query(Job).limit(top_k).all()
            return [(job, 0.5) for job in fallback_jobs]

        scored_candidates = []
        for job_id in all_job_ids:
            score = 0.0
            if job_id in dense_ranks:
                score += cls.rrf_score(dense_ranks[job_id], k=rrf_k)
            if job_id in lexical_ranks:
                score += cls.rrf_score(lexical_ranks[job_id], k=rrf_k)
            scored_candidates.append((job_id, score))

        # Sort by highest RRF score
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = scored_candidates[:top_k]

        # Fetch full Job objects
        top_job_ids = [c[0] for c in top_candidates]
        jobs_dict = {j.id: j for j in db.query(Job).filter(Job.id.in_(top_job_ids)).all()}

        results = []
        for job_id, score in top_candidates:
            if job_id in jobs_dict:
                results.append((jobs_dict[job_id], score))

        return results

hybrid_search = HybridSearchService()
