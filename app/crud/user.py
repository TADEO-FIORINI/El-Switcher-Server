from app.models.user import get_db
from app.schemas.user import UserIn, UserPublic, UserPrivate
from uuid import uuid4

"""USERS CRUD"""

def create_user(user_in: UserIn) -> UserPrivate:
    user_id = str(uuid4())
    with get_db() as cursor:
        cursor.execute("""
            INSERT INTO users (user_id, username, password)
            VALUES (?, ?, ?)
        """, (user_id, user_in.username, user_in.password))
      
        return UserPrivate(user_id=user_id, username=user_in.username, password=user_in.password)

def get_user_by_name(username: str) -> UserPublic:
    with get_db() as cursor:
        cursor.execute("""
            SELECT username
            FROM users 
            WHERE username = ?
        """, (username,))
        user = cursor.fetchone()    
      
        if user:
            return UserPublic(username=user[0])
        return None

    
def get_user_by_id(user_id: str) -> UserPrivate:
    with get_db() as cursor:
        cursor.execute("""
            SELECT user_id, username, password
            FROM users
            WHERE user_id = ?
        """, (user_id,))
        user = cursor.fetchone()    
      
        if not user:
            return None
        return UserPrivate(
            user_id=user[0],
            username=user[1],
            password=user[2]
        )

def get_user_access(username: str, password: str) -> UserPrivate:
    with get_db() as cursor:
        cursor.execute("""
            SELECT user_id, username, password
            FROM users
            WHERE username = ? AND password = ?  
        """, (username, password))
        user = cursor.fetchone()
        
        if not user:
            return None
        return UserPrivate(
            user_id=user[0],
            username=user[1],
            password=user[2]
        )


def delete_user(user_id: str):
    with get_db() as cursor:
        cursor.execute("""
            DELETE FROM users
            WHERE user_id = ?
        """, (user_id,))

