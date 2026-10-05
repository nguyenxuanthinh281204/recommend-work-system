from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class SkillBase(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True

class JobBase(BaseModel):
    title: str
    company: str
    location: str = "Remote"
    salary_range: Optional[str] = None
    experience_level: str = "Mid-Level"
    job_type: str = "Full-time"
    requirements_clean: str
    source_url: Optional[str] = None

class JobCreate(JobBase):
    description_raw: str
    skills: List[str] = []

class JobResponse(JobBase):
    id: int
    description_raw: str
    posted_date: Optional[date]
    created_at: Optional[datetime]
    skills: List[SkillBase] = []

    class Config:
        from_attributes = True

class JobSearchResult(BaseModel):
    job: JobResponse
    lexical_score: Optional[float] = 0.0
    vector_score: Optional[float] = 0.0
    combined_score: float = 0.0
