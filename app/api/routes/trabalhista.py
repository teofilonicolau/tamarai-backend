# app/api/routes/trabalhista.py - VERSÃO COMPLETA COM ETHICS
from fastapi import APIRouter, HTTPException
from app.modules.trabalhista.schemas import DadosTrabalhistas, PeticaoTrabalhista
from app.modules.trabalhista.service import TrabalhistaService
from app.core.ethics import EthicsService

router = APIRouter()
trabalhista_service = TrabalhistaService()

@router.post("/peticao-vinculo")
async def gerar_peticao_vinculo(dados: DadosTrabalhistas):
    """Gera petição de reconhecimento de vínculo empregatício"""
    try:
        peticao = await trabalhista_service.gerar_peticao_vinculo(dados)
        response = {
            "tipo": "peticao_vinculo_empregaticio",
            "area": "trabalhista",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quesitos-insalubridade")
async def gerar_quesitos_insalubridade(dados: DadosTrabalhistas):
    """Gera quesitos para perícia de insalubridade"""
    try:
        quesitos = await trabalhista_service.gerar_quesitos_insalubridade(dados)
        response = {
            "tipo": "quesitos_insalubridade",
            "area": "trabalhista",
            "quesitos": quesitos,
            "total_quesitos": len(quesitos)
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))