# migrate_to_postgresql.py - CRIAR NA RAIZ
import sqlite3
import psycopg2
from app.core.config import settings

def migrate_data():
    """Migra dados do SQLite para PostgreSQL"""
    
    # Conectar ao SQLite
    sqlite_conn = sqlite3.connect('tamaruse.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Conectar ao PostgreSQL
    pg_conn = psycopg2.connect(
        host="localhost",
        database="tamaruse",
        user="tamaruse_user",
        password="tamaruse_pass"
    )
    pg_cursor = pg_conn.cursor()
    
    try:
        # Migrar consultas (se existirem)
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='consultas'")
        if sqlite_cursor.fetchone():
            sqlite_cursor.execute("SELECT * FROM consultas")
            consultas = sqlite_cursor.fetchall()
            
            for consulta in consultas:
                pg_cursor.execute("""
                    INSERT INTO consultas (pergunta, resposta, area_juridica, created_at)
                    VALUES (%s, %s, %s, %s)
                """, consulta[1:5])  # Ajustar índices conforme necessário
        
        pg_conn.commit()
        print("Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"Erro na migração: {e}")
        pg_conn.rollback()
    
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    migrate_data()