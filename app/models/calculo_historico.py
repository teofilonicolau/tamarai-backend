# app/models/calculo_historico.py
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CalculoHistorico(Base):
    __tablename__ = "calculos_historicos"
    
    id = Column(Integer, primary_key=True)
    tipo_calculo = Column(String(50))  # "ec103", "valor_causa", etc.
    dados_entrada = Column(JSON)
    resultado = Column(JSON)
    feedback_score = Column(Integer)  # 1-5 estrelas
    created_at = Column(DateTime, default=datetime.utcnow)