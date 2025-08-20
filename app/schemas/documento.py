# app/schemas/documento.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.documento import TipoDocumento, StatusProcessamento

class DocumentoBase(BaseModel):
    nome_original: str = Field(..., min_length=1, max_length=255)

class DocumentoCreate(DocumentoBase):
    pass

class DocumentoResponse(BaseModel):
    id: int
    nome_original: str
    nome_arquivo: str
    tipo_documento: TipoDocumento
    tamanho_bytes: int
    status_processamento: StatusProcessamento
    texto_extraido: Optional[str]
    resumo_ia: Optional[str]
    area_juridica_detectada: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentoAnalise(BaseModel):
    resumo: str
    pontos_relevantes: list
    area_juridica: str
    palavras_chave: list