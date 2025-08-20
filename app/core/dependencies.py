# app/core/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ai_service import AIService
from app.services.cache_service import CacheService
from app.services.rag_service import RAGService

# Instâncias dos serviços
ai_service_instance = None
cache_service_instance = None
rag_service_instance = None

def get_ai_service() -> AIService:
    global ai_service_instance
    if ai_service_instance is None:
        ai_service_instance = AIService()
    return ai_service_instance

def get_cache_service() -> CacheService:
    global cache_service_instance
    if cache_service_instance is None:
        cache_service_instance = CacheService()
    return cache_service_instance

def get_rag_service() -> RAGService:
    global rag_service_instance
    if rag_service_instance is None:
        rag_service_instance = RAGService()
    return rag_service_instance

# Dependency para database
def get_database() -> Session:
    return Depends(get_db)