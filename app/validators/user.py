from fastapi import HTTPException, status
from app.crud.user import get_user_by_name, get_user_by_id

def format_username(username: str) -> str:
    username_formated = username.strip()
    if len(username_formated) < 3: 
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username is too short")
    if 10 < len(username_formated): 
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username is too long")
    return username_formated

def check_username_is_free(username: str):
    if get_user_by_name(username) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username already exists")

def check_confirm_password(password: str, confirm_password: str):
    if (password != confirm_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Passwords are not the same")

def check_user_exists(user_id: str):
    user_private = get_user_by_id(user_id)
    if user_private is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
def wrong_access(username: str):
    if get_user_by_name(username) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Wrong password")


