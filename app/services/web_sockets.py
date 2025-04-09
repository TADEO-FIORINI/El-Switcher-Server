from fastapi import WebSocket
from typing import Dict, List
from starlette.websockets import WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.global_connections: Dict[str, WebSocket] = {}  # user_id -> WebSocket
        self.room_connections: Dict[str, List[str]] = {}  # room_id -> [user_id]

    async def connect(self, websocket: WebSocket, user_id: str):
        """Conectar usuario al broadcast global."""
        await websocket.accept()
        self.global_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        """Desconectar usuario de todos los broadcasts."""
        if user_id in self.global_connections:
            del self.global_connections[user_id]
        for room_id in list(self.room_connections.keys()):
            if user_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(user_id)
                if not self.room_connections[room_id]:  # Si la sala queda vacía, eliminarla
                    del self.room_connections[room_id]
    async def join_room_broadcast(self, user_id: str, room_id: str):
        """Mover un usuario al broadcast de una sala, saliendo de cualquier otra sala previamente unida."""
        # Eliminar usuario de todas las salas previas
        for rid in list(self.room_connections.keys()):
            if user_id in self.room_connections[rid]:
                self.room_connections[rid].remove(user_id)
                if not self.room_connections[rid]:
                    del self.room_connections[rid]

        # Agregar usuario a la nueva sala
        if room_id not in self.room_connections:
            self.room_connections[room_id] = []
        self.room_connections[room_id].append(user_id)


    async def leave_room_broadcast(self, user_id: str, room_id: str):
        """Eliminar un usuario del broadcast de una sala."""
        if room_id in self.room_connections and user_id in self.room_connections[room_id]:
            self.room_connections[room_id].remove(user_id)
            if not self.room_connections[room_id]:  # Si la sala queda vacía, eliminarla
                del self.room_connections[room_id]

    async def broadcast_global(self, message: str):
        """Enviar mensaje a todos los usuarios en el broadcast global."""
        disconnected_users = []
        for user_id, websocket in self.global_connections.items():
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                disconnected_users.append(user_id)
            except Exception:
                disconnected_users.append(user_id)
        for user_id in disconnected_users:
            self.disconnect(user_id)

    async def broadcast_to_room(self, room_id: str, message: str):
        """Enviar mensaje solo a los usuarios dentro de una sala específica."""
        disconnected_users = []
        if room_id in self.room_connections:
            for user_id in self.room_connections[room_id][:]:
                if user_id in self.global_connections:
                    try:
                        await self.global_connections[user_id].send_text(message)
                    except WebSocketDisconnect:
                        disconnected_users.append(user_id)
                    except Exception:
                        disconnected_users.append(user_id)
            for user_id in disconnected_users:
                self.disconnect(user_id)

manager = ConnectionManager()
