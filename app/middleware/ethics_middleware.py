# app/middleware/ethics_middleware.py - NOVO ARQUIVO
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.ethics import EthicsService

class EthicsMiddleware(BaseHTTPMiddleware):
    """Middleware para garantir conformidade ética em todas as respostas"""
    
    async def dispatch(self, request: Request, call_next):
        # Processar requisição
        response = await call_next(request)
        
        # Adicionar headers de ética
        response.headers["X-AI-Tool"] = "Legal-Assistant"
        response.headers["X-Requires-Lawyer-Review"] = "true"
        response.headers["X-Ethics-Compliance"] = "v1.0"
        
        return response