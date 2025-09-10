# app/schemas/consulta.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ConsultaCreate(BaseModel):
    pergunta: str
    area: str = "geral"
    contexto: Optional[str] = None

class ConsultaResponse(BaseModel):
    id: int
    pergunta: str
    resposta: str
    area: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ConsultaEspecializada(BaseModel):
    pergunta: str
    area: str = "previdenciario"
    contexto: Optional[str] = None
    incluir_jurisprudencia: bool = True
    incluir_legislacao: bool = True
    nivel_detalhamento: str = Field(default="medio", pattern="^(basico|medio|avancado)$")
    
class ConsultaCompleta(BaseModel):
    pergunta: str
    area: str
    resposta: str
    jurisprudencia: Optional[list] = None
    legislacao: Optional[list] = None
    referencias: Optional[list] = None
    confiabilidade: float
    timestamp: datetime