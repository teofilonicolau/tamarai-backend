# app/core/dependencies.py - ARQUIVO NOVO
from app.services.ai_service import ai_service

def get_ai_service():
    """Dependency para obter o serviço de IA"""
    return ai_service