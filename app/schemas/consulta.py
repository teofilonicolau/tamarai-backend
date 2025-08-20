# app/schemas/consulta.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.consulta import AreaJuridica

class ConsultaBase(BaseModel):
    pergunta: str = Field(..., min_length=10, max_length=2000)
    area_juridica: AreaJuridica

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaResponse(BaseModel):
    id: int
    pergunta: str
    resposta: Optional[str]
    area_juridica: AreaJuridica
    palavras_chave: Optional[List[str]]
    jurisprudencia_utilizada: Optional[List[Dict[str, Any]]]
    legislacao_aplicada: Optional[List[Dict[str, Any]]]
    tempo_resposta: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConsultaEspecializada(BaseModel):
    """Schema para consultas especializadas por área"""
    pergunta: str
    contexto_adicional: Optional[str] = None
    incluir_jurisprudencia: bool = True
    incluir_legislacao: bool = True
    nivel_detalhamento: str = Field(default="medio", regex="^(basico|medio|avancado)$")