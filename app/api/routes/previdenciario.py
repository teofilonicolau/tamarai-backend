# app/api/routes/previdenciario.py - VERSÃO COMPLETA
from fastapi import APIRouter, HTTPException
from app.modules.previdenciario.schemas import DadosPrevidenciarios, PeticaoPrevidenciaria
from app.modules.previdenciario.service import PrevidenciarioService
from app.core.ethics import EthicsService

router = APIRouter()
previdenciario_service = PrevidenciarioService()

# ENDPOINTS JÁ EXISTENTES
@router.post("/peticao-aposentadoria-invalidez")
async def gerar_peticao_aposentadoria_invalidez(dados: DadosPrevidenciarios):
    """Gera petição para aposentadoria por invalidez"""
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
    """Gera petição para Revisão da Vida Toda"""
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

@router.post("/peticao-aposentadoria-tempo-contribuicao")
async def gerar_peticao_aposentadoria_tempo_contribuicao(dados: DadosPrevidenciarios):
    """Gera petição para aposentadoria por tempo de contribuição"""
    try:
        peticao = await previdenciario_service.gerar_peticao_aposentadoria_tempo_contribuicao(dados)
        response = {
            "tipo": "peticao_aposentadoria_tempo_contribuicao",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-auxilio-doenca")
async def gerar_peticao_auxilio_doenca(dados: DadosPrevidenciarios):
    """Gera petição para auxílio-doença"""
    try:
        peticao = await previdenciario_service.gerar_peticao_auxilio_doenca(dados)
        response = {
            "tipo": "peticao_auxilio_doenca",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-pensao-morte")
async def gerar_peticao_pensao_morte(dados: DadosPrevidenciarios):
    """Gera petição para pensão por morte"""
    try:
        peticao = await previdenciario_service.gerar_peticao_pensao_morte(dados)
        response = {
            "tipo": "peticao_pensao_morte",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-aposentadoria-especial")
async def gerar_peticao_aposentadoria_especial(dados: DadosPrevidenciarios):
    """Gera petição para aposentadoria especial"""
    try:
        peticao = await previdenciario_service.gerar_peticao_aposentadoria_especial(dados)
        response = {
            "tipo": "peticao_aposentadoria_especial",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-bpc-loas")
async def gerar_peticao_bpc_loas(dados: DadosPrevidenciarios):
    """Gera petição para BPC-LOAS"""
    try:
        peticao = await previdenciario_service.gerar_peticao_bpc_loas(dados)
        response = {
            "tipo": "peticao_bpc_loas",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-aposentadoria-rural")
async def gerar_peticao_aposentadoria_rural(dados: DadosPrevidenciarios):
    """Gera petição para aposentadoria híbrida/rural"""
    try:
        peticao = await previdenciario_service.gerar_peticao_aposentadoria_rural(dados)
        response = {
            "tipo": "peticao_aposentadoria_rural",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-salario-maternidade")
async def gerar_peticao_salario_maternidade(dados: DadosPrevidenciarios):
    """Gera petição para salário-maternidade"""
    try:
        peticao = await previdenciario_service.gerar_peticao_salario_maternidade(dados)
        response = {
            "tipo": "peticao_salario_maternidade",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/peticao-revisao-beneficio")
async def gerar_peticao_revisao_beneficio(dados: DadosPrevidenciarios):
    """Gera petição para revisão de benefício (genérica)"""
    try:
        peticao = await previdenciario_service.gerar_peticao_revisao_beneficio(dados)
        response = {
            "tipo": "peticao_revisao_beneficio",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict()
        }
        return EthicsService.add_ethics_metadata(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ENDPOINT PREMIUM COM CALCULADORA
@router.post("/peticao-com-calculo/{tipo_peticao}")
async def gerar_peticao_com_calculo(
    tipo_peticao: str,
    dados: DadosPrevidenciarios,
    incluir_calculo: bool = True
):
    """Gera petição com integração à calculadora previdenciária"""
    try:
        # Mapear tipo de petição para método correspondente
        metodos_peticao = {
            "aposentadoria-tempo-contribuicao": previdenciario_service.gerar_peticao_aposentadoria_tempo_contribuicao,
            "auxilio-doenca": previdenciario_service.gerar_peticao_auxilio_doenca,
            "pensao-morte": previdenciario_service.gerar_peticao_pensao_morte,
            "aposentadoria-especial": previdenciario_service.gerar_peticao_aposentadoria_especial,
            "bpc-loas": previdenciario_service.gerar_peticao_bpc_loas,
            "aposentadoria-rural": previdenciario_service.gerar_peticao_aposentadoria_rural,
            "salario-maternidade": previdenciario_service.gerar_peticao_salario_maternidade,
            "revisao-beneficio": previdenciario_service.gerar_peticao_revisao_beneficio,
            "aposentadoria-invalidez": previdenciario_service.gerar_peticao_aposentadoria_invalidez,
            "revisao-vida-toda": previdenciario_service.gerar_peticao_revisao_vida_toda
        }
        
        if tipo_peticao not in metodos_peticao:
            raise HTTPException(status_code=400, detail=f"Tipo de petição '{tipo_peticao}' não encontrado")
        
        # 1. Gerar petição normal
        peticao = await metodos_peticao[tipo_peticao](dados)
        
        # 2. Preparar resposta base
        response = {
            "tipo": f"peticao_{tipo_peticao.replace('-', '_')}_premium",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict(),
            "calculo_disponivel": incluir_calculo,
            "valor_calculado": None,
            "planilha_url": None
        }
        
        # 3. Se incluir cálculo, integrar com calculadora
        if incluir_calculo:
            # TODO: Integrar com sua calculadora quando estiver deployada
            response["valor_calculado"] = {
                "rmi_estimada": "R$ 2.850,00",
                "valor_atrasado": "R$ 15.200,00",
                "observacao": "Cálculo será disponibilizado via calculadora especializada"
            }
            response["planilha_url"] = "/calculadora/gerar-planilha"
        
        return EthicsService.add_ethics_metadata(response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))