from pydantic import BaseModel
from .user import UserPrivate, UserPublic
from .enum import GameColor

class RoomPublic(BaseModel):
    room_id: str
    room_name: str
    room_color: GameColor
    room_users: list[UserPublic]

class RoomPrivate(BaseModel):
    room_id: str
    room_name: str
    room_color: GameColor
    room_users: list[UserPrivate]