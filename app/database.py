import sqlite3
from contextlib import contextmanager
import os

# Configurar la base de datos con una variable de entorno o un valor predeterminado
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prod.db")

@contextmanager
def get_db():
    """Gestor de contexto para la base de datos SQLite"""
    # Usar una base de datos diferente para las pruebas 
    db_path = "test.db" if "test" in os.getenv("DATABASE_URL", "") else "prod.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        conn.close()
