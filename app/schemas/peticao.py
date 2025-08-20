# app/schemas/peticao.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from app.models.peticao import TipoPeticao, StatusPeticao
from app.models.consulta import AreaJuridica

# Schemas para dados específicos de cada área
class DadosAutor(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    cpf: str = Field(..., regex=r'^\d{11}$')
    rg: str = Field(..., min_length=5, max_length=20)
    orgao_emissor: str = Field(..., max_length=50)
    nacionalidade: str = Field(default="brasileira")
    estado_civil: str
    profissao: str
    endereco_completo: str
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
    telefone: str
    pis: Optional[str] = Field(None, regex=r'^\d{11}$')

class DadosBeneficioPrevidenciario(BaseModel):
    tipo_beneficio: str
    der: date  # Data de Entrada do Requerimento
    numero_processo_administrativo: Optional[str]
    motivo_recusa: str
    historico_laboral: Optional[str]
    historico_contribuicoes: Optional[str]
    informacoes_medicas: Optional[str]

class DadosConsumidor(BaseModel):
    tipo_problema: str
    empresa_ré: str
    cnpj_empresa: str = Field(..., regex=r'^\d{14}$')
    endereco_empresa: str
    descricao_problema: str
    valor_prejuizo: Optional[float]
    data_ocorrencia: date

class PedidosPeticao(BaseModel):
    pedido_principal: str
    pedido_retroativo: bool = True
    gratuidade_justica: bool = True
    tutela_urgencia: bool = False
    audiencia_conciliacao: bool = True
    valor_causa: float

class PeticaoCreate(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=255)
    tipo: TipoPeticao
    area_juridica: AreaJuridica
    
    # Dados estruturados
    dados_autor: DadosAutor
    dados_especificos: Dict[str, Any]  # Varia por área jurídica
    pedidos: PedidosPeticao
    documentos_anexos: Optional[List[str]] = []
    
    @validator('dados_especificos')
    def validate_dados_especificos(cls, v, values):
        area = values.get('area_juridica')
        if area == AreaJuridica.PREVIDENCIARIO:
            # Validar se tem campos obrigatórios do previdenciário
            required_fields = ['tipo_beneficio', 'der', 'motivo_recusa']
            for field in required_fields:
                if field not in v:
                    raise ValueError(f'Campo {field} obrigatório para área previdenciária')
        elif area == AreaJuridica.CONSUMIDOR:
            # Validar campos do consumidor
            required_fields = ['tipo_problema', 'empresa_ré', 'cnpj_empresa']
            for field in required_fields:
                if field not in v:
                    raise ValueError(f'Campo {field} obrigatório para área do consumidor')
        return v

class PeticaoResponse(BaseModel):
    id: int
    titulo: str
    tipo: TipoPeticao
    area_juridica: AreaJuridica
    status: StatusPeticao
    texto_gerado: Optional[str]
    pdf_path: Optional[str]
    jurisprudencia_utilizada: Optional[List[Dict[str, Any]]]
    legislacao_aplicada: Optional[List[Dict[str, Any]]]
    aprovado_por_humano: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PeticaoAprovacao(BaseModel):
    aprovado: bool
    observacoes: Optional[str] = None