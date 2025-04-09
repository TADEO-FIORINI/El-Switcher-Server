from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    confirm_password: str

class UserPublic(BaseModel):
    username: str

class UserPrivate(BaseModel):
    user_id: str
    username: str
    password: str