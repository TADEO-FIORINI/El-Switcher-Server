from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from .conftest import set_up_test_db, create_testing_users
from app.crud.user import get_user_access

client = TestClient(app)

def test_get_user_access(set_up_test_db):
    create_testing_users()
    user = get_user_access("username1", "password1")

    response = client.get(f"/user/{user.username}/{user.password}")
    assert response.status_code == status.HTTP_200_OK

def test_no_get_user_access_with_wrong_username(set_up_test_db):
    create_testing_users()
    user = get_user_access("username1", "password1")
    
    username = "username"
    response = client.get(f"/user/{username}/{user.password}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_no_get_user_access_with_wrong_password(set_up_test_db):
    create_testing_users()
    user = get_user_access("username1", "password1")

    password = "password"
    response = client.get(f"/user/{user.username}/{password}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED