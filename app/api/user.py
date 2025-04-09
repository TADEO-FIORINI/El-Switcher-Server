from fastapi import APIRouter, status
from app.schemas.user import UserIn, UserPrivate
from app.crud.user import create_user, get_user_access, delete_user
from app.validators.user import check_user_exists, check_username_is_free, check_confirm_password, format_username, wrong_access

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/{username}/{password}/{confirm_password}", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(username: str, password: str, confirm_password: str):
    username = format_username(username)
    check_username_is_free(username)
    check_confirm_password(password, confirm_password)
    user_in = UserIn(username=username, password=password, confirm_password=confirm_password)
    return create_user(user_in)

@router.get("/{username}/{password}", response_model=UserPrivate)
def get_user_access_endpoint(username: str, password: str):
    username = format_username(username)
    user_private = get_user_access(username, password)
    if user_private is None:
        wrong_access(username)
    return user_private

@router.delete("/{user_id}", response_model=str)
def delete_user_endpoint(user_id: str):
    check_user_exists(user_id)
  
    delete_user(user_id)
    return "user_deleted"
