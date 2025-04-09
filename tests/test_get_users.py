from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from .conftest import set_up_test_db, create_testing_users
from app.crud.user import get_user_by_id, get_user_access
from app.crud.helpers.user_helpers import user_private_to_public
from uuid import uuid4 

client = TestClient(app)

def test_get_user_by_id(set_up_test_db):
    create_testing_users()
    user = get_user_access("username1", "password1")

    assert get_user_by_id(user.user_id) == user


def test_no_get_user_by_wrong_id(set_up_test_db):
    user_id = str(uuid4())

    user = get_user_by_id(user_id)
    assert user is None