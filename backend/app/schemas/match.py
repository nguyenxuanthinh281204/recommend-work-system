from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.job import JobResponse

class ExtractedCandidateProfile(BaseModel):
    name: Optional[str] = "Candidate"
    email: Optional[str] = None
    years_of_experience: Optional[float] = 0.0
    detected_skills: List[str] = []
    summary: Optional[str] = None

class JobMatchReasoning(BaseModel):
    match_score: int = Field(description="Score from 0 to 100 representing job fit")
    matched_strengths: List[str] = Field(description="Key skills and qualifications the candidate satisfies")
    skill_gaps: List[str] = Field(description="Missing technologies or requirements")
    career_advice: str = Field(description="Specific actionable advice to pass the interview or improve profile")

class JobMatchItem(BaseModel):
    job: JobResponse
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    reasoning: JobMatchReasoning

class CVMatchResponse(BaseModel):
    candidate: ExtractedCandidateProfile
    top_matches: List[JobMatchItem]
    total_evaluated: int
