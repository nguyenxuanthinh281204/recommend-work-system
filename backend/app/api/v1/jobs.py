from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobResponse, JobSearchResult
from app.services.hybrid_search import hybrid_search

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("", response_model=List[JobResponse])
def get_jobs(
    skip: int = 0,
    limit: int = 20,
    experience_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job)
    if experience_level:
        query = query.filter(Job.experience_level == experience_level)
    return query.order_by(Job.id.desc()).offset(skip).limit(limit).all()

@router.get("/search", response_model=List[JobSearchResult])
def search_jobs(
    q: str = Query(..., description="Semantic or keyword search query (e.g. 'Senior Python Docker')"),
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Search jobs using Hybrid Search (Dense vector + Lexical tsvector)
    """
    results = hybrid_search.search(db, query_text=q, top_k=limit)
    response = []
    for job, score in results:
        response.append(
            JobSearchResult(
                job=JobResponse.model_validate(job),
                combined_score=round(score, 4)
            )
        )
    return response

@router.get("/{job_id}", response_model=JobResponse)
def get_job_detail(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
