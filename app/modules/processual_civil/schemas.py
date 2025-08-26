# app/modules/processual_civil/schemas.py - CRIAR
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class DadosProcessualCivil(BaseModel):
    tipo_peticao: str = Field(..., description="execucao, monitoria, despejo, tutela_urgencia, etc.")
    numero_processo: Optional[str] = None
    parte_contraria: str
    cpf_cnpj_parte_contraria: str = Field(..., pattern=r'^\d{11}$|^\d{14}$')
    endereco_parte_contraria: str
    descricao_pedido: str
    valor_execucao: Optional[float] = None
    titulo_executivo: Optional[str] = None
    data_vencimento: Optional[date] = None
    imovel_endereco: Optional[str] = None  # Para despejo
    valor_aluguel: Optional[float] = None  # Para despejo
    meses_atraso: Optional[int] = None  # Para despejo
    documentos_anexos: Optional[List[str]] = []
    urgencia_fundamentacao: Optional[str] = None

class PeticaoProcessualCivil(BaseModel):
    dados_processual: DadosProcessualCivil
    pedidos_principais: List[str]
    valor_causa: float
    tutela_urgencia: bool = False