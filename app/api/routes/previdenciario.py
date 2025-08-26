# app/api/routes/previdenciario.py - CRIAR
from fastapi import APIRouter, HTTPException
from app.modules.previdenciario.schemas import DadosPrevidenciarios
from app.modules.previdenciario.service import PrevidenciarioService
from app.core.ethics import EthicsService

router = APIRouter()
previdenciario_service = PrevidenciarioService()

@router.post("/peticao-aposentadoria-invalidez")
async def gerar_peticao_aposentadoria_invalidez(dados: DadosPrevidenciarios):
    """Gera petição de aposentadoria por invalidez"""
    try:
        peticao = await previdenciario_service.gerar_peticao_aposentadoria_invalidez(dados)
        response = {
            "tipo": "peticao_aposentadoria_invalidez",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-revisao-vida-toda")
async def gerar_peticao_revisao_vida_toda(dados: DadosPrevidenciarios):
    """Gera petição de Revisão da Vida Toda"""
    try:
        peticao = await previdenciario_service.gerar_peticao_revisao_vida_toda(dados)
        response = {
            "tipo": "peticao_revisao_vida_toda",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))