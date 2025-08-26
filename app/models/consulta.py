# app/models/consulta.py

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class AreaJuridica(str, enum.Enum):
    PREVIDENCIARIO = "previdenciario"
    CONSUMIDOR = "consumidor"
    PROCESSUAL_CIVIL = "processual_civil"
    TRABALHISTA = "trabalhista"

class Consulta(Base):
    __tablename__ = "consultas"
    
    id = Column(Integer, primary_key=True, index=True)
    pergunta = Column(Text, nullable=False)
    resposta = Column(Text, nullable=True)
    area_juridica = Column(Enum(AreaJuridica), nullable=False)
    
    # Metadados da consulta
    palavras_chave = Column(JSON, nullable=True)
    jurisprudencia_utilizada = Column(JSON, nullable=True)
    legislacao_aplicada = Column(JSON, nullable=True)
    
    # Controle
    tempo_resposta = Column(Integer, nullable=True)  # em segundos
    satisfacao_usuario = Column(Integer, nullable=True)  # 1-5
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())