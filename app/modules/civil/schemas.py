# app/modules/civil/schemas.py - CRIAR
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class DadosCivil(BaseModel):
    tipo_acao: str = Field(..., description="cobranca, indenizacao, divorcio, inventario, etc.")
    parte_contraria: str
    cpf_cnpj_parte_contraria: str = Field(..., pattern=r'^\d{11}$|^\d{14}$')
    endereco_parte_contraria: str
    descricao_caso: str
    valor_causa: float
    data_fato_gerador: date
    documentos_comprobatorios: Optional[List[str]] = []
    tentativa_acordo_extrajudicial: bool = False
    urgencia_caso: bool = False
    
    # Específicos por tipo
    valor_divida: Optional[float] = None  # Para cobrança
    valor_danos_materiais: Optional[float] = None  # Para indenização
    valor_danos_morais: Optional[float] = None  # Para indenização
    regime_casamento: Optional[str] = None  # Para divórcio
    filhos_menores: bool = False  # Para divórcio
    bens_inventario: Optional[List[str]] = []  # Para inventário

class PeticaoCivil(BaseModel):
    dados_civil: DadosCivil
    pedidos_principais: List[str]
    valor_causa: float
    tutela_urgencia: bool = False