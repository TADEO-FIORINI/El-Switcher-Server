from fastapi import APIRouter, status
import asyncio
from app.schemas.room import RoomPublic  
from app.crud.user import get_user_by_id
from app.validators.room import check_room_exists, check_room_is_full, check_room_owner, check_no_room_owner, check_room_no_user_dup, \
    check_user_in_room, check_room_name
from app.validators.user import check_user_exists
from app.services.web_sockets import manager
from app.services.room import create_room, get_room, get_public_data_rooms, join_room, leave_room, delete_room, room_private_to_public, \
    force_delete_room_after

router = APIRouter(prefix="/room", tags=["Room"])

@router.post("/{user_id}/{room_name}", response_model=RoomPublic, status_code=status.HTTP_201_CREATED)
async def create_room_endpoint(user_id: str, room_name: str):
    formated_room_name = check_room_name(room_name)
    check_user_exists(user_id)
  
    owner_user = get_user_by_id(user_id)
    room = create_room(formated_room_name, owner_user)
    await manager.join_room_broadcast(user_id, room.room_id)
    await manager.broadcast_global(f"room_created: {room.room_id}")

    asyncio.create_task(force_delete_room_after(room.room_id, delay_seconds=5))

    return room_private_to_public(room)

@router.get("/{user_id}/{room_id}", response_model=RoomPublic)
def get_rooms_endpoint(user_id: str, room_id: str):
    check_user_exists(user_id)
    check_room_exists(room_id)
 
    room = get_room(room_id)
    return room_private_to_public(room)

@router.get("/{user_id}/", response_model=list[RoomPublic])
def get_room_endpoint(user_id: str):
    check_user_exists(user_id)
    
    return get_public_data_rooms()

@router.put("/join/{user_id}/{room_id}", response_model=RoomPublic)
async def join_room_endpoint(user_id: str, room_id: str):
    check_user_exists(user_id)
    check_room_exists(room_id)
    check_room_is_full(room_id)
    check_room_no_user_dup(user_id, room_id)
  
    join_room(user_id, room_id)
    await manager.join_room_broadcast(user_id, room_id)
    await manager.broadcast_global(f"user_joined: {room_id}")

    return room_private_to_public(get_room(room_id))

@router.put("/leave/{user_id}/{room_id}", response_model=str)
async def leave_room_endpoint(user_id: str, room_id: str):
    check_user_exists(user_id)
    check_room_exists(room_id)
    check_user_in_room(user_id, room_id)
    check_no_room_owner(user_id, room_id)
   
    leave_room(user_id, room_id)
    await manager.leave_room_broadcast(user_id, room_id)
    await manager.broadcast_global(f"user_left: {room_id}")

    return "user_left"


@router.delete("/{user_id}/{room_id}", response_model=str)
async def delete_room_endpoint(user_id: str, room_id: str):
    check_user_exists(user_id)
    check_room_exists(room_id)
    check_user_in_room(user_id, room_id)
    check_room_owner(user_id, room_id)
   
    delete_room(room_id) 
    await manager.broadcast_global(f"room_deleted: {room_id}")

    return "room_deleted"