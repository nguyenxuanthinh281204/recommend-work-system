from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base

job_skills = Table(
    "job_skills",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
    Column("is_required", Boolean, default=True)
)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(100), default="Remote")
    salary_range = Column(String(100), nullable=True)
    experience_level = Column(String(50), default="Mid-Level")
    job_type = Column(String(50), default="Full-time")
    description_raw = Column(Text, nullable=False)
    requirements_clean = Column(Text, nullable=False)
    source_url = Column(Text, nullable=True)
    posted_date = Column(Date, server_default=func.current_date())
    
    # 1536-dimensional vector for embedding
    embedding = Column(Vector(1536), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    skills = relationship("Skill", secondary=job_skills, back_populates="jobs")
