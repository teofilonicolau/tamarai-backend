# app/modules/consumidor/schemas.py - NOVO
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class DadosConsumidor(BaseModel):
    tipo_problema: str = Field(..., description="vicio_produto, cobranca_indevida, dano_moral, etc.")
    empresa_ré: str
    cnpj_empresa: str = Field(..., pattern=r'^\d{14}$')
    endereco_empresa: str
    descricao_problema: str
    valor_prejuizo: Optional[float] = None
    data_ocorrencia: date
    tentativa_solucao_amigavel: bool = False
    provas_disponíveis: Optional[List[str]] = []
    valor_produto_servico: Optional[float] = None
    nota_fiscal: bool = False
    garantia_vigente: bool = False

class PeticaoConsumidor(BaseModel):
    dados_consumidor: DadosConsumidor
    pedidos_principais: List[str]
    valor_causa: float
    tutela_urgencia: bool = False