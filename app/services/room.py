from typing import Dict
from uuid import uuid4
from random import choice
import asyncio
from .web_sockets import manager
from .user import user_private_to_public
from app.schemas.user import UserPrivate
from app.schemas.room import RoomPrivate, RoomPublic
from app.schemas.enum import GameColor
from app.crud.user import get_user_by_id

rooms: Dict[str, RoomPrivate] = {}

def create_room(room_name: str, owner_user: UserPrivate) -> RoomPrivate:
    room_id = str(uuid4())
    room = RoomPrivate(room_id=room_id, room_name=room_name, room_users=[owner_user], room_color=choice(list(GameColor)))
    rooms[room_id] = room
    return room

def get_room(room_id: str) -> RoomPrivate:
    return rooms.get(room_id)

def get_public_data_rooms() -> list[RoomPublic]:
    return [room_private_to_public(room) for room in rooms.values()]

def join_room(user_id: str, room_id: str):
    user = get_user_by_id(user_id)
    room = get_room(room_id)
    room.room_users.append(user)

def leave_room(user_id: str, room_id: str):
    user = get_user_by_id(user_id)
    room = get_room(room_id)
    room.room_users.remove(user)

def delete_room(room_id: str):
    if room_id in rooms:
        del rooms[room_id]

def room_private_to_public(room_private: RoomPrivate) -> RoomPublic:
    room_id = room_private.room_id
    room_name = room_private.room_name
    room_users = [user_private_to_public(user) for user in room_private.room_users]
    room_color = room_private.room_color
    room_public = RoomPublic(room_id=room_id, room_name=room_name, room_users=room_users, room_color=room_color)
    return room_public

async def force_delete_room_after(room_id: str, delay_seconds: int):
    await asyncio.sleep(delay_seconds)
    delete_room(room_id)
    await manager.broadcast_to_room(room_id, f"room_expired: {room_id}")
