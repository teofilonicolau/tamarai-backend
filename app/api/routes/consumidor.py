# app/api/routes/consumidor.py - CRIAR
from fastapi import APIRouter, HTTPException
from app.modules.consumidor.schemas import DadosConsumidor
from app.modules.consumidor.service import ConsumidorService
from app.core.ethics import EthicsService

router = APIRouter()
consumidor_service = ConsumidorService()

@router.post("/peticao-vicio-produto")
async def gerar_peticao_vicio_produto(dados: DadosConsumidor):
    """Gera petição para vício do produto"""
    try:
        peticao = await consumidor_service.gerar_peticao_vicio_produto(dados)
        response = {
            "tipo": "peticao_vicio_produto",
            "area": "consumidor",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-cobranca-indevida")
async def gerar_peticao_cobranca_indevida(dados: DadosConsumidor):
    """Gera petição para cobrança indevida"""
    try:
        peticao = await consumidor_service.gerar_peticao_cobranca_indevida(dados)
        response = {
            "tipo": "peticao_cobranca_indevida",
            "area": "consumidor",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))