# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI(
    title="TamarAI - Inteligência Artificial Aplicada",  # ← ATUALIZADO
    description="Soluções inteligentes para automação, análise de dados e integração de sistemas",  # ← ATUALIZADO
    version="1.0.0",  # ← RESET PARA NOVA IDENTIDADE
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

# Rotas básicas
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API TamarAI!",  # ← ATUALIZADO
        "version": "1.0.0",
        "status": "Operacional",
        "purpose": "Inteligência Artificial aplicada com propósito",  # ← ATUALIZADO
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tamarai-backend"}  # ← ATUALIZADO

@app.get("/test")
async def test_endpoint():
    return {
        "message": "Endpoint de teste da TamarAI funcionando!",  # ← ATUALIZADO
        "database": "SQLite configurado",
        "static_files": "Configurado"
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