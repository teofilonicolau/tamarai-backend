# app/modules/previdenciario/schemas.py - VERSÃO COMPLETA
from pydantic import BaseModel, validator
from typing import Optional, List

class DadosPrevidenciarios(BaseModel):
    # Campos do benefício
    tipo_beneficio: str
    numero_beneficio: Optional[str] = None
    der: Optional[str] = None
    dib: Optional[str] = None
    numero_processo_administrativo: Optional[str] = None
    motivo_recusa: Optional[str] = None
    
    # Dados pessoais
    nome: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    orgao_emissor: Optional[str] = None
    endereco_completo: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[str] = None  # Para cálculo de idade/prioridade
    
    # Dados contributivos
    tempo_contribuicao_total: Optional[int] = None
    historico_laboral: Optional[str] = None
    historico_contribuicoes: Optional[str] = None
    
    # Dados médicos
    informacoes_medicas: Optional[str] = None
    laudos_medicos: Optional[List[str]] = []
    cid_principal: Optional[str] = None
    
    # Atividade especial
    atividade_especial: Optional[bool] = False
    exposicao_agentes_nocivos: Optional[str] = None
    
    # Valor da causa
    valor_causa: Optional[float] = None
    
    # Campos adicionais
    justica_gratuita: bool = True  # Padrão True para previdenciário
    tutela_antecipada: bool = True  # Padrão True para urgência
    especialidade_perito: Optional[str] = None  # "ortopedista", "neurologista", etc.
    
    # NOVO CAMPO PARA COMARCA
    comarca: Optional[str] = None
    cidade_comarca: Optional[str] = None
    estado_comarca: Optional[str] = None
    
    # Validações
    @validator('cpf')
    def validar_cpf(cls, v):
        if v and len(v.replace('.', '').replace('-', '')) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        return v
    
    @validator('valor_causa')
    def validar_valor_causa(cls, v):
        if v and v <= 0:
            raise ValueError('Valor da causa deve ser positivo')
        return v

class PeticaoPrevidenciaria(BaseModel):
    tipo: str
    area: str
    texto_peticao: str
    dados_utilizados: DadosPrevidenciarios