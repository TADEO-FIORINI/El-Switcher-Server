from uuid import uuid4
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from .conftest import set_up_test_db, create_testing_rooms
from app.crud.user import get_user_access
from app.crud.room import get_room, rooms
from app.crud.helpers.user_helpers import user_private_to_public

client = TestClient(app)

def test_join_room(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()
    user = get_user_access("username2", "password2")

    response = client.put(f"/room/join/{user.user_id}/{room.room_id}")
    assert response.status_code == status.HTTP_200_OK
    assert user_private_to_public(user).model_dump() in response.json()["room_users"]

def test_no_join_inexistent_user(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()
    user_id = str(uuid4())
    
    response = client.put(f"/room/join/{user_id}/{room.room_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
def test_no_join_inexistent_room(set_up_test_db):
    rooms.clear()
    create_testing_rooms()
    user = get_user_access("username2", "password2")
    room_id = str(uuid4())

    response = client.put(f"/room/join/{user.user_id}/{room_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_no_join_full_room(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()

    user = get_user_access("username2", "password2")
    client.put(f"/room/join/{user.user_id}/{room.room_id}")

    user = get_user_access("username3", "password3")
    client.put(f"/room/join/{user.user_id}/{room.room_id}")

    user = get_user_access("username4", "password4")
    client.put(f"/room/join/{user.user_id}/{room.room_id}")

    user = get_user_access("username5", "password5")
    response = client.put(f"/room/join/{user.user_id}/{room.room_id}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_no_join_dup_user(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()

    user = get_user_access("username2", "password2")
    client.put(f"/room/join/{user.user_id}/{room.room_id}")

    user = get_user_access("username2", "password2")
    response = client.put(f"/room/join/{user.user_id}/{room.room_id}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

