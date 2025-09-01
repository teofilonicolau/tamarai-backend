# app/api/routes/calculadora.py - VERSÃO EXPANDIDA
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import date

# Importar todas as calculadoras
from app.core.calculators.previdenciario_calculator import CalculadoraPrevidenciaria
from app.core.calculators.previdenciario_ec103_calculator import CalculadoraPrevidenciariaEC103
from app.core.calculators.trabalhista_calculator import CalculadoraTrabalhista
from app.core.calculators.trabalhista_completa_calculator import CalculadoraTrabalhistaCompleta
from app.core.calculators.base_calculator import BaseCalculator

router = APIRouter()

# Instanciar calculadoras
calc_prev = CalculadoraPrevidenciaria()
calc_prev_ec103 = CalculadoraPrevidenciariaEC103()
calc_trab = CalculadoraTrabalhista()
calc_trab_completa = CalculadoraTrabalhistaCompleta()
calc_base = BaseCalculator()

# Schemas para requests
class TempoEspecialRequest(BaseModel):
    tempo_rural: int = 0
    tempo_urbano: int = 0
    tempo_especial: int = 0

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

# =================== ENDPOINTS PREVIDENCIÁRIOS ===================

@router.post("/api/v1/calculadora/tempo-especial")
async def calcular_tempo_especial(dados: TempoEspecialRequest):
    """Endpoint público para cálculo de tempo especial"""
    try:
        resultado = calc_prev.somar_tempos_contributivos(
            rural=dados.tempo_rural,
            urbano=dados.tempo_urbano, 
            especial=dados.tempo_especial
        )
        return {
            "calculo": resultado,
            "uso": "calculadora_publica",
            "status": "sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/calculadora/periodo-graca")
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

@router.post("/api/v1/calculadora/valor-causa")
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

@router.post("/api/v1/calculadora/regra-transicao-ec103")
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

# =================== ENDPOINTS TRABALHISTAS ===================

@router.post("/api/v1/calculadora/horas-extras")
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

@router.post("/api/v1/calculadora/verbas-rescisorias")
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

# =================== ENDPOINTS GERAIS ===================

@router.get("/api/v1/calculadora/status")
async def status_calculadoras():
    """Status de todas as calculadoras disponíveis"""
    return {
        "calculadoras_disponiveis": {
            "previdenciario": [
                "tempo-especial",
                "periodo-graca", 
                "valor-causa",
                "regra-transicao-ec103"
            ],
            "trabalhista": [
                "horas-extras",
                "verbas-rescisorias"
            ],
            "geral": [
                "juros-mora",
                "correcao-monetaria"
            ]
        },
        "total_endpoints": 6,
        "status": "operacional"
    }

@router.get("/api/v1/calculadora/info")
async def info_calculadoras():
    """Informações sobre as calculadoras"""
    return {
        "previdenciario": {
            "ec103_implementada": True,
            "regras_transicao": ["pedagogio_50", "pedagogio_100", "regra_geral", "regra_pontos"],
            "observacao": "Inclui todas as regras da EC 103/2019"
        },
        "trabalhista": {
            "verbas_completas": True,
            "inclui": ["aviso_previo", "ferias", "13_salario", "fgts", "multa"],
            "observacao": "Cálculo completo de rescisão"
        },
        "versao": "2.0.0",
        "ultima_atualizacao": "2024-12-19"
    }