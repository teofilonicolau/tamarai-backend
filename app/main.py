# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Importar o serviço de IA
from app.services.ai_service import ai_service

app = FastAPI(
    title="TamarAI - Inteligência Artificial Aplicada",
    description="Soluções inteligentes para automação, análise de dados e integração de sistemas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar diretórios se não existirem
os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("static/pdfs", exist_ok=True)

# Modelos Pydantic
class ConsultaRequest(BaseModel):
    pergunta: str
    area: str = "geral"

class AnaliseRequest(BaseModel):
    texto: str
    tipo_analise: str = "resumo"

class RelatorioRequest(BaseModel):
    titulo: str
    conteudo: str
    area: str = "geral"
    incluir_jurisprudencia: bool = True

# Rotas básicas
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API TamarAI!",
        "version": "1.0.0",
        "status": "Operacional",
        "purpose": "Inteligência Artificial aplicada com propósito",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tamarai-backend"}

@app.get("/test")
async def test_endpoint():
    return {
        "message": "Endpoint de teste da TamarAI funcionando!",
        "database": "SQLite configurado",
        "static_files": "Configurado"
    }

@app.get("/debug/env")
async def debug_env():
    """Debug - verificar variáveis de ambiente"""
    return {
        "openai_key_exists": bool(os.getenv("OPENAI_API_KEY")),
        "openai_key_length": len(os.getenv("OPENAI_API_KEY", "")),
        "openai_model": os.getenv("OPENAI_MODEL", "não encontrado")
    }

# ROTAS DE IA
@app.post("/api/v1/consulta")
async def fazer_consulta(request: ConsultaRequest):
    """Consulta jurídica com IA real"""
    resultado = await ai_service.fazer_consulta_juridica(request.pergunta, request.area)
    
    return {
        "pergunta": request.pergunta,
        "area": request.area,
        **resultado
    }

@app.post("/api/v1/analise")
async def analisar_texto(request: AnaliseRequest):
    """Análise de documento com IA real"""
    resultado = await ai_service.analisar_documento(request.texto, request.tipo_analise)
    
    return {
        "texto_original": request.texto[:100] + "..." if len(request.texto) > 100 else request.texto,
        **resultado
    }

@app.post("/api/v1/relatorio")
async def gerar_relatorio(request: RelatorioRequest):
    """Gerar relatório jurídico estruturado"""
    resultado = await ai_service.gerar_relatorio_juridico(
        request.titulo, 
        request.conteudo, 
        request.area,
        request.incluir_jurisprudencia
    )
    
    return {
        "titulo": request.titulo,
        "area": request.area,
        **resultado
    }

@app.get("/api/v1/status")
async def api_status():
    """Status da API e serviços"""
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    
    return {
        "api": "online",
        "database": "sqlite - conectado",
        "ai_service": "openai - configurado" if openai_configured else "openai - não configurado",
        "cache": "não configurado",
        "version": "1.0.0"
    }

# Servir arquivos estáticos
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Aviso: Não foi possível montar arquivos estáticos: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
