# app/modules/previdenciario/schemas.py - NOVO
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class DadosPrevidenciarios(BaseModel):
    tipo_beneficio: str = Field(..., description="aposentadoria_invalidez, tempo_contribuicao, revisao_vida_toda, etc.")
    numero_beneficio: Optional[str] = None
    der: date  # Data de Entrada do Requerimento
    dib: Optional[date] = None  # Data de Início do Benefício
    numero_processo_administrativo: Optional[str] = None
    motivo_recusa: str
    tempo_contribuicao_total: Optional[int] = None  # em meses
    historico_laboral: Optional[str] = None
    historico_contribuicoes: Optional[str] = None
    informacoes_medicas: Optional[str] = None
    laudos_medicos: Optional[List[str]] = []
    cid_principal: Optional[str] = None
    atividade_especial: bool = False
    exposicao_agentes_nocivos: Optional[str] = None

class PeticaoPrevidenciaria(BaseModel):
    dados_previdenciarios: DadosPrevidenciarios
    pedidos_principais: List[str]
    valor_causa: float
    tutela_urgencia: bool = False