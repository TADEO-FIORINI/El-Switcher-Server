from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from .conftest import set_up_test_db, create_testing_users
from app.crud.user import get_user_access
from app.validators.room import room_private_to_public
from app.crud.room import get_room, rooms
from uuid import uuid4

client = TestClient(app)

def test_create_room(set_up_test_db):
    rooms.clear()
    create_testing_users()
    user = get_user_access("username1", "password1")
    room_name = "room"

    response = client.post(f"/room/{user.user_id}/{room_name}")
    assert response.status_code == status.HTTP_201_CREATED

def test_no_create_room_with_no_user(set_up_test_db):
    rooms.clear()
    user_id = str(uuid4())
    room_name = "room"

    response = client.post(f"/room/{user_id}/{room_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
