# app/modules/trabalhista/schemas.py - VERSÃO CORRIGIDA
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class DadosTrabalhistas(BaseModel):
    tipo_acao: str = Field(..., description="vínculo, horas_extras, rescisao_indireta, etc.")
    empresa_ré: str
    cnpj_empresa: str = Field(..., pattern=r'^\d{14}$')  # CORRIGIDO: regex → pattern
    periodo_trabalho_inicio: date
    periodo_trabalho_fim: Optional[date] = None
    cargo_funcao: str
    salario_registrado: Optional[float] = None
    salario_real: Optional[float] = None
    jornada_contratual: str = Field(default="44h semanais")
    jornada_real: Optional[str] = None
    horas_extras_habituais: bool = False
    adicional_insalubridade: bool = False
    adicional_periculosidade: bool = False
    equipamentos_seguranca: bool = True
    testemunhas: Optional[List[str]] = []
    documentos_comprobatorios: Optional[List[str]] = []

class PeticaoTrabalhista(BaseModel):
    dados_trabalhistas: DadosTrabalhistas
    pedidos_principais: List[str]
    valor_causa: float
    tutela_urgencia: bool = False