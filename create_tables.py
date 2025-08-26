# create_tables.py - CRIAR NA RAIZ DO PROJETO
from app.core.database import engine
from app.models.base import Base
from app.models import consulta, peticao, documento

print("Criando tabelas no PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")