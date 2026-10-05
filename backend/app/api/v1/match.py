from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.match import CVMatchResponse, JobMatchItem
from app.schemas.job import JobResponse
from app.services.cv_parser import cv_parser
from app.services.hybrid_search import hybrid_search
from app.services.explainer import explainer_service

router = APIRouter(prefix="/match", tags=["CV Matching & Explainability"])

@router.post("/cv", response_model=CVMatchResponse)
async def match_cv(
    file: Optional[UploadFile] = File(None),
    cv_text: Optional[str] = Form(None),
    top_k: int = Form(10),
    db: Session = Depends(get_db)
):
    """
    Accepts candidate CV (PDF, DOCX, or direct raw text),
    extracts key skills, runs Hybrid Retrieval against JDs in PostgreSQL + pgvector,
    and returns Top 10 matches with LLM explainability.
    """
    extracted_text = ""
    if file:
        content = await file.read()
        filename = file.filename.lower()
        if filename.endswith(".pdf"):
            extracted_text = cv_parser.extract_text_from_pdf(content)
        elif filename.endswith(".docx"):
            extracted_text = cv_parser.extract_text_from_docx(content)
        else:
            extracted_text = content.decode("utf-8", errors="ignore")
    elif cv_text:
        extracted_text = cv_text
    else:
        raise HTTPException(status_code=400, detail="Please upload a CV file or provide cv_text.")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Unable to extract text from provided CV.")

    # 1. Parse CV and detect canonical skills
    candidate = cv_parser.parse_cv_content(extracted_text)

    # 2. Hybrid Search for candidate pool (Vector + Lexical)
    matched_job_tuples = hybrid_search.search(
        db,
        query_text=candidate.summary or extracted_text[:1000],
        query_skills=candidate.detected_skills,
        top_k=top_k
    )

    # 3. LLM Reasoning for each Top candidate
    items = []
    cand_skill_set = set(candidate.detected_skills)
    
    for job, _score in matched_job_tuples:
        job_skill_names = [s.name for s in job.skills]
        matched_skills = list(cand_skill_set.intersection(set(job_skill_names)))
        missing_skills = list(set(job_skill_names).difference(cand_skill_set))

        reasoning = explainer_service.explain_match(candidate, job)
        
        items.append(
            JobMatchItem(
                job=JobResponse.model_validate(job),
                match_score=reasoning.match_score,
                matched_skills=matched_skills,
                missing_skills=missing_skills,
                reasoning=reasoning
            )
        )

    # Sort final items by match_score descending
    items.sort(key=lambda x: x.match_score, reverse=True)

    return CVMatchResponse(
        candidate=candidate,
        top_matches=items,
        total_evaluated=len(items)
    )
