from ..database import get_db

def create_tables():
    with get_db() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """)
        
create_tables()
