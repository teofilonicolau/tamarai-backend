
# app/api/routes/previdenciario.py - VERSÃO COMPLETA
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.modules.previdenciario.schemas import DadosPrevidenciarios, PeticaoPrevidenciaria
from app.modules.previdenciario.service import PrevidenciarioService
from app.core.ethics import EthicsService
from app.services.pdf_service import PDFService
import io
from datetime import date

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
    incluir_calculo: bool = Query(False)
):
    """Gera petição com integração à calculadora previdenciária"""
    try:
        # ADICIONAR MAPEAMENTO CORRETO:
        mapeamento_tipos = {
            "aposentadoria-por-tempo": "aposentadoria_tempo_contribuicao",
            "aposentadoria-invalidez": "aposentadoria_invalidez",
            "auxilio-doenca": "auxilio_doenca",
            "pensao-morte": "pensao_morte",
            "aposentadoria-especial": "aposentadoria_especial",
            "bpc-loas": "bpc_loas",
            "aposentadoria-rural": "aposentadoria_rural",
            "salario-maternidade": "salario_maternidade",
            "revisao-vida-toda": "revisao_vida_toda",
            "revisao-beneficio": "revisao_beneficio"
        }
        
        # VERIFICAR SE TIPO EXISTE:
        if tipo_peticao not in mapeamento_tipos:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de petição '{tipo_peticao}' não encontrado"
            )
        
        # CHAMAR MÉTODO CORRETO:
        tipo_interno = mapeamento_tipos[tipo_peticao]
        
        # Mapear tipo interno para método correspondente
        metodos_peticao = {
            "aposentadoria_tempo_contribuicao": previdenciario_service.gerar_peticao_aposentadoria_tempo_contribuicao,
            "aposentadoria_invalidez": previdenciario_service.gerar_peticao_aposentadoria_invalidez,
            "auxilio_doenca": previdenciario_service.gerar_peticao_auxilio_doenca,
            "pensao_morte": previdenciario_service.gerar_peticao_pensao_morte,
            "aposentadoria_especial": previdenciario_service.gerar_peticao_aposentadoria_especial,
            "bpc_loas": previdenciario_service.gerar_peticao_bpc_loas,
            "aposentadoria_rural": previdenciario_service.gerar_peticao_aposentadoria_rural,
            "salario_maternidade": previdenciario_service.gerar_peticao_salario_maternidade,
            "revisao_vida_toda": previdenciario_service.gerar_peticao_revisao_vida_toda,
            "revisao_beneficio": previdenciario_service.gerar_peticao_revisao_beneficio
        }
        
        if tipo_interno not in metodos_peticao:
            raise HTTPException(status_code=400, detail=f"Método para '{tipo_interno}' não implementado")
        
        # 1. Gerar petição normal
        peticao = await metodos_peticao[tipo_interno](dados)
        
        # 2. Preparar resposta base
        response = {
            "tipo": f"peticao_{tipo_interno}_premium",
            "area": "previdenciario",
            "texto_peticao": peticao,
            "dados_utilizados": dados.dict(),
            "calculo_disponivel": incluir_calculo,
            "valor_calculado": None,
            "planilha_url": None
        }
        
        # 3. Se incluir cálculo, integrar com calculadora
        if incluir_calculo:
            # TODO: Integrar com calculadora especializada quando estiver deployada
            response["valor_calculado"] = {
                "rmi_estimada": "R$ 2.850,00",
                "valor_atrasado": "R$ 15.200,00",
                "observacao": "Cálculo será disponibilizado via calculadora especializada"
            }
            response["planilha_url"] = "/calculadora/gerar-planilha"
        
        return EthicsService.add_ethics_metadata(response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ENDPOINT PDF ====================
@router.post("/peticao-pdf/{tipo_peticao}")
async def gerar_pdf_peticao(
    tipo_peticao: str,
    dados: DadosPrevidenciarios
):
    """
    Gera PDF da petição aprovada para download
    """
    
    # Mapear tipo de petição para função
    funcoes_peticao = {
        "aposentadoria-especial": previdenciario_service.gerar_peticao_aposentadoria_especial,
        "aposentadoria-invalidez": previdenciario_service.gerar_peticao_aposentadoria_invalidez,
        "auxilio-doenca": previdenciario_service.gerar_peticao_auxilio_doenca,
        "pensao-morte": previdenciario_service.gerar_peticao_pensao_morte,
        "bpc-loas": previdenciario_service.gerar_peticao_bpc_loas,
        "aposentadoria-rural": previdenciario_service.gerar_peticao_aposentadoria_rural,
        "salario-maternidade": previdenciario_service.gerar_peticao_salario_maternidade,
        "revisao-vida-toda": previdenciario_service.gerar_peticao_revisao_vida_toda,
        "aposentadoria-tempo-contribuicao": previdenciario_service.gerar_peticao_aposentadoria_tempo_contribuicao,
        "revisao-beneficio": previdenciario_service.gerar_peticao_revisao_beneficio
    }
    
    if tipo_peticao not in funcoes_peticao:
        raise HTTPException(status_code=400, detail="Tipo de petição inválido")
    
    # Gerar petição
    funcao_peticao = funcoes_peticao[tipo_peticao]
    resultado = await funcao_peticao(dados)
    
    # Extrair texto da petição
    texto_peticao = resultado  # Já é string direta do service
    
    # Gerar PDF
    pdf_service = PDFService()
    
    # Nome do arquivo
    nome_cliente = dados.nome.replace(" ", "_") if dados.nome else "cliente"
    nome_arquivo = f"peticao_{tipo_peticao}_{nome_cliente}_{date.today().strftime('%Y%m%d')}.pdf"
    nome_arquivo = nome_arquivo.lower()
    
    # Gerar PDF usando o serviço existente
    pdf_path = await pdf_service.gerar_peticao_pdf(
        dados_peticao=dados.dict(),
        texto_peticao=texto_peticao,
        nome_arquivo=nome_arquivo
    )
    
    # Ler arquivo PDF
    with open(pdf_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()
    
    # Retornar PDF para download
    headers = {
        'Content-Disposition': f'attachment; filename="{nome_arquivo}"'
    }
    
    return StreamingResponse(
        io.BytesIO(pdf_content),
        media_type="application/pdf",
        headers=headers
    )