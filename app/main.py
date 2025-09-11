# app/main.py - VERSÃO CORRIGIDA
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

# Importar o serviço de IA
from app.services.ai_service import ai_service

# Importar routers
from app.api.routes import calculadora, peticoes, consultas
from app.api.routes import trabalhista, consumidor, previdenciario, civil, processual_civil
from app.api.routes import analytics
from app.middleware.ethics_middleware import EthicsMiddleware

app = FastAPI(
    title="TamarUSE API",
    description="Soluções inteligentes para automação jurídica com IA",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Adicionar middleware ético
app.add_middleware(EthicsMiddleware)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://tamarai-frontend-92ho41oeq.vercel.app",
        "https://*.vercel.app",
        "https://tamarai-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Criar diretórios estáticos
os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("static/pdfs", exist_ok=True)

# Modelos Pydantic
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
        "message": "Bem-vindo à API TamarUSE!",
        "version": "2.0.0",
        "status": "Operacional",
        "purpose": "Inteligência Artificial aplicada com propósito",
        "docs": "/docs",
        "novidades": "Calculadoras EC 103/2019 e Trabalhista Completa",
        "endpoints": {
            "consulta": "/api/v1/consulta",
            "analise": "/api/v1/analise",
            "parecer_juridico": "/api/v1/parecer-juridico",
            "areas_direito": "/api/v1/areas-direito",
            "calculadoras": "/api/v1/calculadora/status",
            "analytics": "/api/v1/analytics",
            "status": "/api/v1/status",
            "debug": "/debug/env"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "tamaruse-backend",
        "calculadoras": "operacionais",
        "analytics": "disponivel",
        "version": "2.0.0"
    }

@app.get("/test")
async def test_endpoint():
    return {
        "message": "Endpoint de teste da TamarUSE funcionando!",
        "database": "PostgreSQL configurado",
        "static_files": "Configurado",
        "calculadoras": "EC 103 + Trabalhista Completa",
        "analytics": "implementado"
    }

@app.get("/debug/env")
async def debug_env():
    return {
        "openai_key_exists": bool(os.getenv("OPENAI_API_KEY")),
        "openai_key_length": len(os.getenv("OPENAI_API_KEY", "")),
        "openai_model": os.getenv("OPENAI_MODEL", "não encontrado"),
        "database_url": os.getenv("DATABASE_URL", "não encontrado"),
        "calculadoras_status": "operacionais",
        "analytics_status": "disponivel"
    }

@app.get("/api/v1/status")
async def api_status():
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "api": "online",
        "database": "postgresql - conectado",
        "ai_service": "openai - configurado" if openai_configured else "openai - não configurado",
        "cache": "redis - configurado",
        "calculadoras": "ec103 + trabalhista completa",
        "analytics": "monitoramento ativo",
        "version": "2.0.0",
        "endpoints_disponiveis": [
            "/api/v1/consulta",
            "/api/v1/analise",
            "/api/v1/parecer-juridico",
            "/api/v1/areas-direito",
            "/api/v1/calculadora/*",
            "/api/v1/analytics/*",
            "/api/v1/trabalhista",
            "/api/v1/consumidor",
            "/api/v1/previdenciario",
            "/api/v1/civil",
            "/api/v1/processual-civil"
        ]
    }

@app.get("/api/v1/areas-direito")
async def listar_areas_direito():
    areas = {
        "previdenciario": {
            "nome": "Direito Previdenciário",
            "descricao": "Benefícios do INSS, aposentadorias, auxílios",
            "tipos_peticao": ["inicial", "revisao", "recurso"],
            "calculadoras": ["tempo-especial", "regra-transicao-ec103", "periodo-graca"]
        },
        "trabalhista": {
            "nome": "Direito Trabalhista",
            "descricao": "Relações de trabalho, rescisões, direitos trabalhistas",
            "tipos_peticao": ["inicial", "contestacao", "recurso"],
            "calculadoras": ["horas-extras", "verbas-rescisorias"]
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
        "service": "TamarUSE - Serviço Jurídico com IA",
        "calculadoras_disponiveis": True,
        "analytics_disponivel": True
    }

# Rotas de IA
@app.post("/api/v1/consulta")
async def fazer_consulta(request: ConsultaRequest):
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

# Incluir routers
app.include_router(calculadora.router, prefix="/api/v1", tags=["calculadoras"])
app.include_router(peticoes.router, prefix="/api/v1", tags=["peticoes"])
app.include_router(consultas.router, prefix="/api/v1", tags=["consultas"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])
app.include_router(trabalhista.router, prefix="/api/v1/trabalhista", tags=["trabalhista"])
app.include_router(consumidor.router, prefix="/api/v1/consumidor", tags=["consumidor"])
app.include_router(previdenciario.router, prefix="/api/v1/previdenciario", tags=["previdenciario"])
app.include_router(civil.router, prefix="/api/v1/civil", tags=["civil"])
app.include_router(processual_civil.router, prefix="/api/v1/processual-civil", tags=["processual-civil"])

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