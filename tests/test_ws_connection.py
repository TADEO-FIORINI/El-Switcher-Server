import pytest
import asyncio
from fastapi.testclient import TestClient
from fastapi import status, WebSocket
from app.main import app
from .conftest import set_up_test_db, create_testing_users
from app.crud.user import get_user_access
from app.crud.room import rooms 

client = TestClient(app)

@pytest.mark.asyncio
async def test_websocket_room_broadcast(set_up_test_db):
    rooms.clear()
    create_testing_users()
    user1 = get_user_access("username1", "password1")
    user2 = get_user_access("username2", "password2")
    room_name = "test_room"

    # Conectar WebSocket para el usuario 1
    with client.websocket_connect(f"/ws/{user1.user_id}") as ws1:
        
        # Crear la sala con el usuario 1
        response = client.post(f"/room/{user1.user_id}/{room_name}")
        assert response.status_code == status.HTTP_201_CREATED
        
        room_id = response.json()["room_id"]
        # Verificar que el WebSocket recibió el mensaje de que se creó la sala
        msg = ws1.receive_text()
        assert msg == "new_room_created"

        # Conectar WebSocket para el usuario 2
        with client.websocket_connect(f"/ws/{user2.user_id}") as ws2:
            
            # Usuario 2 se une a la sala
            response = client.put(f"/room/join/{user2.user_id}/{room_id}")
            assert response.status_code == status.HTTP_200_OK

            # Ambos WebSockets deberían recibir el mensaje de que el usuario 2 se unió
            msg1 = ws1.receive_text()
            msg2 = ws2.receive_text()
            assert msg1 == f"user_joined: {room_id}"
            assert msg2 == f"user_joined: {room_id}"
