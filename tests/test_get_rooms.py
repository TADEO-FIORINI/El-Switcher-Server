from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from .conftest import set_up_test_db, create_testing_rooms
from app.crud.user import get_user_access
from app.crud.room import get_room, rooms
from app.validators.room import room_private_to_public
from uuid import uuid4

client = TestClient(app)

def test_get_room(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()
    user = get_user_access("username1", "password1")

    response = client.get(f"/room/{user.user_id}/{room.room_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == room_private_to_public(room).model_dump()


def test_no_get_inexistent_room(set_up_test_db):
    rooms.clear()
    _, _, _ = create_testing_rooms()
    user = get_user_access("username1", "password1")
    room_id = str(uuid4())

    response = client.get(f"/room/{user.user_id}/{room_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_no_get_inexistent_user(set_up_test_db):
    rooms.clear()
    room, _, _ = create_testing_rooms()
    user_id = str(uuid4())

    response = client.get(f"/room/{user_id}/{room.room_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
