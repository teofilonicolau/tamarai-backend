# app/api/routes/processual_civil.py - CRIAR
from fastapi import APIRouter, HTTPException
from app.modules.processual_civil.schemas import DadosProcessualCivil
from app.modules.processual_civil.service import ProcessualCivilService
from app.core.ethics import EthicsService

router = APIRouter()
processual_service = ProcessualCivilService()

@router.post("/peticao-execucao")
async def gerar_peticao_execucao(dados: DadosProcessualCivil):
    """Gera petição de execução"""
    try:
        peticao = await processual_service.gerar_peticao_execucao(dados)
        response = {
            "tipo": "peticao_execucao",
            "area": "processual_civil",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-monitoria")
async def gerar_peticao_monitoria(dados: DadosProcessualCivil):
    """Gera petição de ação monitória"""
    try:
        peticao = await processual_service.gerar_peticao_monitoria(dados)
        response = {
            "tipo": "peticao_monitoria",
            "area": "processual_civil",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))