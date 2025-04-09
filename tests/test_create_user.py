from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from .conftest import set_up_test_db, create_testing_users
from app.crud.user import get_user_by_name, get_user_access

client = TestClient(app)

def test_create_user(set_up_test_db):
    username = "username"
    password = "password"
    confirm_password = password
    # llamar endpoint
    response = client.post(f"/user/{username}/{password}/{confirm_password}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()[username] == username
    assert response.json()[password] == password
    # Verificar que el usuario se guardó en la base de prueba
    user = get_user_by_name(username)
    assert user is not None
    assert user.username == username

def test_no_create_dup_user(set_up_test_db):
    create_testing_users()
    user = get_user_access("username1", "password1")
    username = user.username
    password = user.password
    confirm_password = password

    client.post(f"/user/{username}/{password}/{confirm_password}")
    response = client.post(f"/user/{username}/{password}/{confirm_password}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_no_create_user_with_wrong_confirm_password(set_up_test_db):
    create_testing_users()
    user = get_user_access("username1", "password1")
    username = user.username
    password = user.password
    confirm_password = password

    confirm_password = "wrong_password"
    response = client.post(f"/user/{username}/{password}/{confirm_password}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_no_create_user_with_bad_username(set_up_test_db):
    create_testing_users()
    user = get_user_access("username1", "password1")
    username = user.username
    password = user.password
    confirm_password = password

    # Menos de 2 caracteres
    username = "t"
    response = client.post(f"/user/{username}/{password}/{confirm_password}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Mas de 13 caracteres
    username = "cocacolacocacola"
    confirm_password = password
    response = client.post(f"/user/{username}/{password}/{confirm_password}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
