# app/api/routes/civil.py - CRIAR
from fastapi import APIRouter, HTTPException
from app.modules.civil.schemas import DadosCivil
from app.modules.civil.service import CivilService
from app.core.ethics import EthicsService

router = APIRouter()
civil_service = CivilService()

@router.post("/peticao-cobranca")
async def gerar_peticao_cobranca(dados: DadosCivil):
    """Gera petição de cobrança"""
    try:
        peticao = await civil_service.gerar_peticao_cobranca(dados)
        response = {
            "tipo": "peticao_cobranca",
            "area": "civil",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-indenizacao")
async def gerar_peticao_indenizacao(dados: DadosCivil):
    """Gera petição de indenização"""
    try:
        peticao = await civil_service.gerar_peticao_indenizacao(dados)
        response = {
            "tipo": "peticao_indenizacao",
            "area": "civil",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))