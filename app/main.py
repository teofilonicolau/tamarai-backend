# app/main.py - VERSÃO SIMPLIFICADA SEM IMPORTS COMPLEXOS

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Importar o serviço de IA (sem imports circulares)
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar diretórios se não existirem
os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("static/pdfs", exist_ok=True)

# Modelos Pydantic SIMPLIFICADOS
class ConsultaRequest(BaseModel):
    pergunta: str
    area: str = "geral"
    firm_name: Optional[str] = None
    lawyer_name: Optional[str] = None
    signature_text: Optional[str] = None
    ai_persona: Optional[str] = None

class AnaliseRequest(BaseModel):
    texto: str
    tipo_analise: str = "resumo"
    firm_name: Optional[str] = None
    lawyer_name: Optional[str] = None
    signature_text: Optional[str] = None
    ai_persona: Optional[str] = None

class RelatorioRequest(BaseModel):
    titulo: str
    conteudo: str
    area: str = "geral"
    incluir_jurisprudencia: bool = True
    firm_name: Optional[str] = None
    lawyer_name: Optional[str] = None
    signature_text: Optional[str] = None
    ai_persona: Optional[str] = None

# Rotas básicas
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API TamarAI!",
        "version": "1.0.0",
        "status": "Operacional",
        "purpose": "Inteligência Artificial aplicada com propósito",
        "docs": "/docs",
        "endpoints": {
            "consulta": "/api/v1/consulta",
            "analise": "/api/v1/analise", 
            "parecer_juridico": "/api/v1/parecer-juridico",
            "areas_direito": "/api/v1/areas-direito",
            "status": "/api/v1/status",
            "debug": "/debug/env"
        }
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
        "openai_model": os.getenv("OPENAI_MODEL", "não encontrado"),
        "database_url": os.getenv("DATABASE_URL", "não encontrado")
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
        "version": "1.0.0",
        "endpoints_disponiveis": [
            "/api/v1/consulta",
            "/api/v1/analise",
            "/api/v1/parecer-juridico",
            "/api/v1/areas-direito"
        ]
    }

@app.get("/api/v1/areas-direito")
async def listar_areas_direito():
    """Listar todas as áreas do direito disponíveis"""
    areas = {
        "previdenciario": {
            "nome": "Direito Previdenciário",
            "descricao": "Benefícios do INSS, aposentadorias, auxílios",
            "tipos_peticao": ["inicial", "revisao", "recurso"]
        },
        "trabalhista": {
            "nome": "Direito Trabalhista", 
            "descricao": "Relações de trabalho, rescisões, direitos trabalhistas",
            "tipos_peticao": ["inicial", "contestacao", "recurso"]
        },
        "consumidor": {
            "nome": "Direito do Consumidor",
            "descricao": "Relações de consumo, vícios, defeitos, indenizações",
            "tipos_peticao": ["inicial", "contestacao"]
        },
        "civil": {
            "nome": "Direito Civil",
            "descricao": "Contratos, responsabilidade civil, família",
            "tipos_peticao": ["inicial", "contestacao", "recurso"]
        },
        "processual_civil": {
            "nome": "Direito Processual Civil",
            "descricao": "Procedimentos, prazos, recursos processuais",
            "tipos_peticao": ["inicial", "contestacao", "recurso", "embargos"]
        }
    }
    return {
        "areas": areas,
        "total_areas": len(areas),
        "service": "TamarAI - Serviço Jurídico com IA"
    }

# ROTAS DE IA
@app.post("/api/v1/consulta")
async def fazer_consulta(request: ConsultaRequest):
    """Consulta jurídica com IA real"""
    resultado = await ai_service.fazer_consulta_juridica(
        request.pergunta, 
        request.area,
        firm_name=request.firm_name,
        lawyer_name=request.lawyer_name,
        signature_text=request.signature_text,
        ai_persona=request.ai_persona
    )
    
    return {
        "pergunta": request.pergunta,
        "area": request.area,
        "escritorio": request.firm_name or "Serviço Jurídico AI",
        **resultado
    }

@app.post("/api/v1/analise")
async def analisar_texto(request: AnaliseRequest):
    """Análise de documento com IA real"""
    resultado = await ai_service.analisar_documento(
        request.texto, 
        request.tipo_analise,
        firm_name=request.firm_name,
        lawyer_name=request.lawyer_name,
        signature_text=request.signature_text,
        ai_persona=request.ai_persona
    )
    
    return {
        "texto_original": request.texto[:100] + "..." if len(request.texto) > 100 else request.texto,
        "escritorio": request.firm_name or "Serviço Jurídico AI",
        **resultado
    }

@app.post("/api/v1/parecer-juridico")
async def gerar_parecer_juridico(request: RelatorioRequest):
    """Gerar parecer jurídico estruturado"""
    resultado = await ai_service.gerar_relatorio_juridico(
        request.titulo, 
        request.conteudo, 
        request.area,
        request.incluir_jurisprudencia,
        firm_name=request.firm_name,
        lawyer_name=request.lawyer_name,
        signature_text=request.signature_text,
        ai_persona=request.ai_persona
    )
    
    return {
        "titulo": request.titulo,
        "area": request.area,
        "tipo": "parecer_juridico",
        "escritorio": request.firm_name or "Serviço Jurídico AI",
        **resultado
    }

# Servir arquivos estáticos
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Aviso: Não foi possível montar arquivos estáticos: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )