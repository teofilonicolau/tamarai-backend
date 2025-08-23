# app/core/config.py - VERSÃO SIMPLIFICADA E CORRIGIDA
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database - CORRIGIDO para usar o nome do seu .env
    database_url: str = "sqlite:///./tamaruse.db"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Application
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Permitir campos extras do .env
        extra = "allow"

# Instância global
settings = Settings()