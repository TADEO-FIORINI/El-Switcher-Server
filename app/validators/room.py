from fastapi import HTTPException, status
from app.crud.user import get_user_by_id
from app.services.room import get_room

def check_room_is_full(room_id: str):
    room = get_room(room_id)
    if (len(room.room_users) >= 4):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Room is full")

def check_room_no_user_dup(user_id: str, room_id: str):       
    user = get_user_by_id(user_id)
    room = get_room(room_id)
    if user in room.room_users:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User already is in the room")

def check_user_in_room(user_id: str, room_id: str):
    user = get_user_by_id(user_id)
    room = get_room(room_id)
    if not user in room.room_users:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User is not in the room")

def check_room_exists(room_id):
    room = get_room(room_id)
    if room is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room

def check_room_owner(user_id: str, room_id: str):
    room = get_room(room_id)
    user = get_user_by_id(user_id)
    user_owner = room.room_users[0]
    if user != user_owner:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Just owner can delete the room")
    
def check_no_room_owner(user_id: str, room_id: str):
    user_owner = get_user_by_id(user_id)
    room = get_room(room_id)
    if room.room_users[0] == user_owner:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Owner can not leave without delete room")
    
def check_room_name(room_name: str) -> str:
    room_name_formated = room_name.strip()
    if len(room_name_formated) < 3: 
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Room name is too short")
    if 12 < len(room_name_formated): 
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Room name is too long")
    return room_name_formated