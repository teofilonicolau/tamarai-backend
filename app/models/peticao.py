# app/models/peticao.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON, Boolean
from sqlalchemy.sql import func
from app.models.base import Base
from app.models.consulta import AreaJuridica
import enum

class TipoPeticao(str, enum.Enum):
    INICIAL = "inicial"
    REPLICA = "replica"
    RECURSO = "recurso"
    QUESITOS = "quesitos"

class StatusPeticao(str, enum.Enum):
    RASCUNHO = "rascunho"
    GERADA = "gerada"
    APROVADA = "aprovada"
    ENVIADA = "enviada"

class Peticao(Base):
    __tablename__ = "peticoes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identificação
    titulo = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoPeticao), nullable=False)
    area_juridica = Column(Enum(AreaJuridica), nullable=False)
    status = Column(Enum(StatusPeticao), default=StatusPeticao.RASCUNHO)
    
    # Dados estruturados do formulário
    dados_formulario = Column(JSON, nullable=False)
    
    # Conteúdo gerado
    texto_gerado = Column(Text, nullable=True)
    pdf_path = Column(String(500), nullable=True)
    
    # Metadados da geração
    jurisprudencia_utilizada = Column(JSON, nullable=True)
    legislacao_aplicada = Column(JSON, nullable=True)
    prompt_utilizado = Column(Text, nullable=True)
    
    # Controle de qualidade
    aprovado_por_humano = Column(Boolean, default=False)
    observacoes_aprovacao = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)