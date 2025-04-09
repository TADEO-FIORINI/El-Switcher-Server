from uuid import uuid4
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from .conftest import set_up_test_db, create_testing_rooms
from app.crud.user import get_user_access
from app.crud.room import join_room, rooms

client = TestClient(app)

def test_delete_room(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()
    user = get_user_access("username1", "password1")

    response = client.delete(f"/room/{user.user_id}/{room.room_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "room_deleted"

def test_no_delete_inexistent_user(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()
    user_id = str(uuid4())

    response = client.delete(f"/room/{user_id}/{room.room_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
def test_no_delete_inexistent_room(set_up_test_db):
    rooms.clear()
    _, _, _ = create_testing_rooms()
    user = get_user_access("username1", "password1")
    room_id = str(uuid4())

    response = client.delete(f"/room/{user.user_id}/{room_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_no_delete_no_owner(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()

    user = get_user_access("username2", "password2")
    join_room(user.user_id, room.room_id)

    response = client.delete(f"/room/{user.user_id}/{room.room_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
