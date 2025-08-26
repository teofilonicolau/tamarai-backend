# app/core/config.py - VERSÃO atualizada
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://tamaruse_user:tamaruse_pass@localhost:5432/tamaruse"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_jurisprudencia: int = 86400  # 24 horas
    cache_ttl_ai_response: int = 3600      # 1 hora
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Application
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

# Instância global
settings = Settings()
