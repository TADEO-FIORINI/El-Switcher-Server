from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from .conftest import set_up_test_db, create_testing_users
from app.crud.user import get_user_access
from uuid import uuid4

client = TestClient(app)

def test_delete_user(set_up_test_db):
    create_testing_users()
    user = get_user_access("username1", "password1")

    response = client.delete(f"/user/{user.user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "user_deleted"

def test_delete_inexistent_user(set_up_test_db):
    create_testing_users()
    user_id = str(uuid4())
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND