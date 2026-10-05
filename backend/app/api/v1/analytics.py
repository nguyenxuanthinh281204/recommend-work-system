from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from app.core.database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics & Market Trends"])

@router.get("/hot-skills")
def get_hot_skills(limit: int = 15, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Returns market demand analytics: Top skills demanded across all parsed JDs.
    """
    sql = text("""
        SELECT s.name, s.category, COUNT(js.job_id) as demand_count
        FROM skills s
        JOIN job_skills js ON s.id = js.skill_id
        GROUP BY s.id, s.name, s.category
        ORDER BY demand_count DESC
        LIMIT :limit
    """)
    rows = db.execute(sql, {"limit": limit}).fetchall()
    
    top_skills = [
        {"skill": r.name, "category": r.category, "count": r.demand_count}
        for r in rows
    ]

    # Category breakdown
    cat_sql = text("""
        SELECT s.category, COUNT(js.job_id) as total_jobs
        FROM skills s
        JOIN job_skills js ON s.id = js.skill_id
        GROUP BY s.category
        ORDER BY total_jobs DESC
    """)
    cat_rows = db.execute(cat_sql).fetchall()
    categories = [
        {"category": r.category, "count": r.total_jobs}
        for r in cat_rows
    ]

    return {
        "top_skills": top_skills,
        "categories": categories
    }
