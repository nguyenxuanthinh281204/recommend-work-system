from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Job Matching System"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres123@localhost:5432/jobmatch_db"
    
    # AI & Embedding Providers: 'openai' or 'mock'
    EMBEDDING_PROVIDER: str = "mock"
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = "mock-key"
    
    # Model Configurations
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIM: int = 1536
    LLM_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
