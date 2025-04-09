from app.database import get_db
from app.models.user import create_tables
from app.schemas import RoomPrivate, UserIn
from app.crud.user import create_user, get_user_access
from app.crud.room import create_room
import pytest
import os
from typing import Tuple

@pytest.fixture(scope="function")
def set_up_test_db():

    # Configurar la base de datos para pruebas con variable de entorno
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"

    # Crear las tablas para pruebas
    with get_db() as cursor:
        create_tables()

    yield

    # Verificar si la base de datos de prueba existe antes de eliminarla
    if os.path.exists("test.db"):
        os.remove("test.db")

    os.environ["DATABASE_URL"] = "sqlite:///./prod.db"
    

""" No usar estas funciones fuera de un test porque se crean cosas en la base de datos real (y sin pasar por los checks de los endpoints) """

def create_testing_users():
    create_user(UserIn(username="username1", password="password1", confirm_password="password1"))
    create_user(UserIn(username="username2", password="password2", confirm_password="password2"))
    create_user(UserIn(username="username3", password="password3", confirm_password="password3"))
    create_user(UserIn(username="username4", password="password4", confirm_password="password4"))
    create_user(UserIn(username="username5", password="password5", confirm_password="password5"))


def create_testing_rooms() -> Tuple[RoomPrivate, RoomPrivate, RoomPrivate]:
    create_testing_users()
    room1 = create_room("room1", get_user_access("username1", "password1"))
    room2 = create_room("room2", get_user_access("username2", "password2"))
    room3 = create_room("room3", get_user_access("username3", "password3"))
    return room1, room2, room3
    