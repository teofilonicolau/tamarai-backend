# app/main.py → VERSÃO FINAL OFICIAL (produção + dev)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

# Importar serviços e rotas
from app.services.ai_service import ai_service
from app.api.routes import (
    calculadora, peticoes, consultas, analytics,
    trabalhista, consumidor, previdenciario, civil, processual_civil
)
from app.middleware.ethics_middleware import EthicsMiddleware

app = FastAPI(
    title="TamarUSE API",
    description="Soluções inteligentes para automação jurídica com IA",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware ético
app.add_middleware(EthicsMiddleware)

# ========== CORS CONFIGURATION (AQUI ESTÁ O QUE IMPORTA) ==========
# Detecta automaticamente se está em desenvolvimento
IS_DEV = os.getenv("ENVIRONMENT") == "development" or not os.getenv("RAILWAY_ENVIRONMENT")

origins = [
    # PRODUÇÃO - Domínios reais (OBRIGATÓRIO)
    "https://law-clerck.vercel.app",           # SEU DOMÍNIO PRINCIPAL ← ADICIONADO!
    "https://lawclerk.vercel.app",              # Possível variação sem hífen
    "https://tamarai-frontend.vercel.app",
    "https://tamarai-frontend-*.vercel.app",
    "https://*.vercel.app",                     # Seguro se você só usa Vercel
]

# DESENVOLVIMENTO LOCAL - Só ativa no seu PC
if IS_DEV:
    origins.extend([
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretórios estáticos
os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("static/pdfs", exist_ok=True)

# Modelos Pydantic (mantidos iguais)
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

# Rotas básicas (mantidas)
@app.get("/")
async def root():
    return {"message": "TamarUSE API rodando!", "version": "2.0.0", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

# Rotas de IA
@app.post("/api/v1/consulta")
async def fazer_consulta(request: ConsultaRequest):
    resultado = await ai_service.fazer_consulta_juridica(
        request.pergunta, request.area,
        firm_name=request.firm_name,
        lawyer_name=request.lawyer_name,
        signature_text=request.signature_text,
        ai_persona=request.ai_persona
    )
    return {"pergunta": request.pergunta, "escritorio": request.firm_name or "LawClerk AI", **resultado}

@app.post("/api/v1/analise")
async def analisar_texto(request: AnaliseRequest):
    resultado = await ai_service.analisar_documento(
        request.texto, request.tipo_analise,
        firm_name=request.firm_name,
        lawyer_name=request.lawyer_name,
        signature_text=request.signature_text,
        ai_persona=request.ai_persona
    )
    return {"escritorio": request.firm_name or "LawClerk AI", **resultado}

@app.post("/api/v1/parecer-juridico")
async def gerar_parecer_juridico(request: RelatorioRequest):
    resultado = await ai_service.gerar_relatorio_juridico(
        request.titulo, request.conteudo, request.area, request.incluir_jurisprudencia,
        firm_name=request.firm_name,
        lawyer_name=request.lawyer_name,
        signature_text=request.signature_text,
        ai_persona=request.ai_persona
    )
    return {"titulo": request.titulo, "escritorio": request.firm_name or "LawClerk AI", **resultado}

# Incluir todos os routers
app.include_router(calculadora.router, prefix="/api/v1", tags=["calculadoras"])
app.include_router(peticoes.router, prefix="/api/v1", tags=["peticoes"])
app.include_router(consultas.router, prefix="/api/v1", tags=["consultas"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])
app.include_router(trabalhista.router, prefix="/api/v1/trabalhista", tags=["trabalhista"])
app.include_router(consumidor.router, prefix="/api/v1/consumidor", tags=["consumidor"])
app.include_router(previdenciario.router, prefix="/api/v1/previdenciario", tags=["previdenciario"])
app.include_router(civil.router, prefix="/api/v1/civil", tags=["civil"])
app.include_router(processual_civil.router, prefix="/api/v1/processual-civil", tags=["processual-civil"])

# Arquivos estáticos
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"[WARN] Static files não montados: {e}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)