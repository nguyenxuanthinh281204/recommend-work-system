from fastapi import APIRouter
from app.api.v1.jobs import router as jobs_router
from app.api.v1.match import router as match_router
from app.api.v1.analytics import router as analytics_router

api_router = APIRouter()
api_router.include_router(jobs_router)
api_router.include_router(match_router)
api_router.include_router(analytics_router)
