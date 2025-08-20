# app/models/documento.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class TipoDocumento(str, enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    IMAGE = "image"

class StatusProcessamento(str, enum.Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    CONCLUIDO = "concluido"
    ERRO = "erro"

class Documento(Base):
    __tablename__ = "documentos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informações do arquivo
    nome_original = Column(String(255), nullable=False)
    nome_arquivo = Column(String(255), nullable=False)
    caminho_arquivo = Column(String(500), nullable=False)
    tipo_documento = Column(Enum(TipoDocumento), nullable=False)
    tamanho_bytes = Column(Integer, nullable=False)
    
    # Processamento
    status_processamento = Column(Enum(StatusProcessamento), default=StatusProcessamento.PENDENTE)
    texto_extraido = Column(Text, nullable=True)
    resumo_ia = Column(Text, nullable=True)
    palavras_chave = Column(Text, nullable=True)
    
    # Análise jurídica
    area_juridica_detectada = Column(String(50), nullable=True)
    pontos_relevantes = Column(Text, nullable=True)
    
    # Controle
    processado_em = Column(DateTime(timezone=True), nullable=True)
    erro_processamento = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())