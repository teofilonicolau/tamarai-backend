# app/api/routes/calculadora.py - VERSÃO EXPANDIDA
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import date

# Importar todas as calculadoras
from app.core.calculators.previdenciario_calculator import CalculadoraPrevidenciaria
from app.core.calculators.previdenciario_ec103_calculator import CalculadoraPrevidenciariaEC103
from app.core.calculators.trabalhista_calculator import CalculadoraTrabalhista
from app.core.calculators.trabalhista_completa_calculator import CalculadoraTrabalhistaCompleta
from app.core.calculators.base_calculator import BaseCalculator
from app.core.calculators.familia_calculator import CalculadoraFamilia
from app.core.calculators.processual_calculator import CalculadoraProcessual

router = APIRouter()

# Instanciar calculadoras
calc_prev = CalculadoraPrevidenciaria()
calc_prev_ec103 = CalculadoraPrevidenciariaEC103()
calc_trab = CalculadoraTrabalhista()
calc_trab_completa = CalculadoraTrabalhistaCompleta()
calc_base = BaseCalculator()
calc_familia = CalculadoraFamilia()
calc_processual = CalculadoraProcessual()

# Schemas para requests
class TempoEspecialRequest(BaseModel):
    tempo_rural: int = 0
    tempo_urbano: int = 0
    tempo_especial: int = 0
    data_inicio_especial: Optional[date] = None

class PeriodoGracaRequest(BaseModel):
    tipo_segurado: str
    ultima_contribuicao: date

class ValorCausaRequest(BaseModel):
    parcelas_vencidas: int
    valor_mensal: float

class RegraTransicaoRequest(BaseModel):
    sexo: str
    idade_atual: int
    tempo_contribuicao_atual: int
    tempo_contribuicao_em_13_11_2019: int

class HorasExtrasRequest(BaseModel):
    jornada_contratual: int
    jornada_real: int
    dias_trabalhados: int
    valor_hora: float

class Verbas_RescisoriasRequest(BaseModel):
    salario: float
    data_admissao: date
    data_rescisao: date
    tipo_rescisao: str = "sem_justa_causa"

class JurosMoraRequest(BaseModel):
    valor_principal: float
    data_vencimento: date
    taxa_mensal: float = 0.01

class CorrecaoMonetariaRequest(BaseModel):
    valor: float
    data_inicial: date
    indice: str = "INPC"

class AdicionalNoturnoRequest(BaseModel):
    salario_base: float
    horas_noturnas: int
    dias_trabalhados: int

class PensaoAlimenticiaRequest(BaseModel):
    renda_alimentante: float
    numero_filhos: int
    percentual_sugerido: float = 0.30

class LiquidacaoSentencaRequest(BaseModel):
    valor_principal: float
    data_sentenca: date
    incluir_honorarios: bool = True

class RevisaoVidaTodaRequest(BaseModel):
    salarios_antes_1994: List[float]
    salarios_depois_1994: List[float]
    data_dib: date

# =================== ENDPOINTS PREVIDENCIÁRIOS ===================

@router.post("/tempo-especial")
async def calcular_tempo_especial(dados: TempoEspecialRequest):
    """Calcular conversão de tempo especial com melhorias"""
    try:
        resultado = calc_prev.somar_tempos_contributivos(
            rural=dados.tempo_rural,
            urbano=dados.tempo_urbano, 
            especial=dados.tempo_especial,
            data_inicio_especial=dados.data_inicio_especial
        )
        
        return {
            "calculo": resultado,
            "uso": "calculadora_publica",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/periodo-graca")
async def calcular_periodo_graca(dados: PeriodoGracaRequest):
    """Verificar se segurado mantém qualidade"""
    try:
        resultado = calc_prev.calcular_periodo_graca(
            tipo_segurado=dados.tipo_segurado,
            ultima_contribuicao=dados.ultima_contribuicao
        )
        return {
            "resultado": resultado,
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/valor-causa")
async def calcular_valor_causa(dados: ValorCausaRequest):
    """Calcular valor da causa para petição"""
    try:
        resultado = calc_prev.calcular_valor_causa(
            parcelas_vencidas=dados.parcelas_vencidas,
            valor_mensal=dados.valor_mensal
        )
        return {
            "valor_causa": resultado,
            "moeda": "BRL",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/regra-transicao-ec103")
async def calcular_regra_transicao_ec103(dados: RegraTransicaoRequest):
    """Calcular melhor regra de transição da EC 103/2019"""
    try:
        resultado = calc_prev_ec103.calcular_regra_transicao(
            sexo=dados.sexo,
            idade_atual=dados.idade_atual,
            tempo_contribuicao_atual=dados.tempo_contribuicao_atual,
            tempo_contribuicao_em_13_11_2019=dados.tempo_contribuicao_em_13_11_2019
        )
        return {
            "resultado": resultado,
            "ec103": True,
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/revisao-vida-toda")
async def calcular_revisao_vida_toda(dados: RevisaoVidaTodaRequest):
    """Calcular revisão da vida toda"""
    try:
        resultado = calc_prev.calcular_revisao_vida_toda(
            salarios_antes_1994=dados.salarios_antes_1994,
            salarios_depois_1994=dados.salarios_depois_1994,
            data_dib=dados.data_dib
        )
        return {
            "calculo": resultado,
            "area": "previdenciario",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =================== ENDPOINTS TRABALHISTAS ===================

@router.post("/horas-extras")
async def calcular_horas_extras(dados: HorasExtrasRequest):
    """Calcular horas extras trabalhistas"""
    try:
        resultado = calc_trab.calcular_horas_extras(
            jornada_contratual=dados.jornada_contratual,
            jornada_real=dados.jornada_real,
            dias_trabalhados=dados.dias_trabalhados,
            valor_hora=dados.valor_hora
        )
        return {
            "calculo": resultado,
            "area": "trabalhista",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verbas-rescisorias")
async def calcular_verbas_rescisorias(dados: Verbas_RescisoriasRequest):
    """Calcular todas as verbas rescisórias"""
    try:
        dados_rescisao = {
            "salario": dados.salario,
            "data_admissao": dados.data_admissao,
            "data_rescisao": dados.data_rescisao,
            "tipo_rescisao": dados.tipo_rescisao
        }
        
        resultado = calc_trab_completa.calcular_verbas_rescisorias_completas(dados_rescisao)
        return {
            "calculo": resultado,
            "area": "trabalhista",
            "tipo": "verbas_completas",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/adicional-noturno")
async def calcular_adicional_noturno(dados: AdicionalNoturnoRequest):
    """Calcular adicional noturno"""
    try:
        resultado = calc_trab.calcular_adicional_noturno(
            salario_base=dados.salario_base,
            horas_noturnas=dados.horas_noturnas,
            dias_trabalhados=dados.dias_trabalhados
        )
        return {
            "calculo": resultado,
            "area": "trabalhista",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =================== ENDPOINTS FAMÍLIA ===================

@router.post("/pensao-alimenticia")
async def calcular_pensao_alimenticia(dados: PensaoAlimenticiaRequest):
    """Calcular pensão alimentícia"""
    try:
        resultado = calc_familia.calcular_pensao_alimenticia(
            renda_alimentante=dados.renda_alimentante,
            numero_filhos=dados.numero_filhos,
            percentual_sugerido=dados.percentual_sugerido
        )
        return {
            "calculo": resultado,
            "area": "familia",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =================== ENDPOINTS PROCESSUAIS ===================

@router.post("/liquidacao-sentenca")
async def calcular_liquidacao_sentenca(dados: LiquidacaoSentencaRequest):
    """Calcular liquidação de sentença"""
    try:
        resultado = calc_processual.calcular_liquidacao_sentenca(
            valor_principal=dados.valor_principal,
            data_sentenca=dados.data_sentenca,
            incluir_honorarios=dados.incluir_honorarios
        )
        return {
            "calculo": resultado,
            "area": "processual",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =================== ENDPOINTS GERAIS ===================

@router.post("/juros-mora")
async def calcular_juros_mora(dados: JurosMoraRequest):
    """Calcular juros de mora"""
    try:
        resultado = calc_base.calcular_juros_mora(
            valor_principal=dados.valor_principal,
            data_vencimento=dados.data_vencimento,
            taxa_mensal=dados.taxa_mensal
        )
        return {
            "calculo": resultado,
            "area": "geral",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/correcao-monetaria")
async def calcular_correcao_monetaria(dados: CorrecaoMonetariaRequest):
    """Aplicar correção monetária"""
    try:
        resultado = calc_base.aplicar_correcao_monetaria(
            valor=dados.valor,
            data_inicial=dados.data_inicial,
            indice=dados.indice
        )
        return {
            "calculo": resultado,
            "area": "geral", 
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def status_calculadoras():
    """Status de todas as calculadoras disponíveis"""
    return {
        "calculadoras_disponiveis": {
            "previdenciario": [
                "tempo-especial",
                "periodo-graca", 
                "valor-causa",
                "regra-transicao-ec103",
                "revisao-vida-toda"
            ],
            "trabalhista": [
                "horas-extras",
                "verbas-rescisorias",
                "adicional-noturno"
            ],
            "familia": [
                "pensao-alimenticia"
            ],
            "processual": [
                "liquidacao-sentenca"
            ],
            "geral": [
                "juros-mora",
                "correcao-monetaria"
            ]
        },
        "total_endpoints": 12,
        "status": "operacional"
    }

@router.get("/info")
async def info_calculadoras():
    """Informações sobre as calculadoras"""
    return {
        "previdenciario": {
            "ec103_implementada": True,
            "regras_transicao": ["pedagogio_50", "pedagogio_100", "regra_geral", "regra_pontos"],
            "revisao_vida_toda": True,
            "observacao": "Inclui todas as regras da EC 103/2019 e revisão da vida toda"
        },
        "trabalhista": {
            "verbas_completas": True,
            "adicional_noturno": True,
            "inclui": ["aviso_previo", "ferias", "13_salario", "fgts", "multa", "adicional_noturno"],
            "observacao": "Cálculo completo de rescisão e adicionais"
        },
        "familia": {
            "pensao_alimenticia": True,
            "observacao": "Cálculo de pensão alimentícia com base em renda e número de filhos"
        },
        "processual": {
            "liquidacao_sentenca": True,
            "observacao": "Cálculo de liquidação de sentença com honorários"
        },
        "geral": {
            "juros_mora": True,
            "correcao_monetaria": True,
            "observacao": "Cálculos financeiros básicos"
        },
        "versao": "2.0.2",
        "ultima_atualizacao": "2025-09-04"
    }