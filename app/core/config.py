# app/core/config.py (CORRIGIR IMPORT)
import os
from pydantic_settings import BaseSettings  # ← MUDANÇA AQUI
from typing import Optional

class Settings(BaseSettings):
    # Database (SQLite para desenvolvimento, PostgreSQL para produção)
    DATABASE_URL: str = "sqlite:///./tamarai.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"  # ← MUDEI PARA 3.5 (mais barato)
    
    # Aplicação
    SECRET_KEY: str = "tamarai-secret-key-change-in-production"
    DEBUG: bool = True
    
    # Diretórios
    STATIC_DIR: str = "static"
    UPLOAD_DIR: str = "uploads"
    PDF_OUTPUT_DIR: str = "static/pdfs"
    
    # Limites
    MAX_FILE_SIZE: int = 30 * 1024 * 1024  # 30MB
    MAX_FILES_PER_CHAT: int = 5
    
    # Cache
    CACHE_TTL_JURISPRUDENCIA: int = 86400  # 24 horas
    CACHE_TTL_AI_RESPONSE: int = 3600      # 1 hora
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Criar diretórios se não existirem
os.makedirs(settings.STATIC_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.PDF_OUTPUT_DIR, exist_ok=True)