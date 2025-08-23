# app/core/database.py - VERSÃO CORRIGIDA
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

# Usar diretamente do .env para evitar imports circulares
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tamaruse.db")

# Engine do banco
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=True  # Para debug
)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependency para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()