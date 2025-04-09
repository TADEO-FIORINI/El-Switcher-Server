from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.web_sockets import manager

router = APIRouter(prefix="/ws", tags=["WebSockets"])

@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """Conectar usuario al broadcast global."""
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()  # Mantener conexión abierta
    except WebSocketDisconnect:
        manager.disconnect(user_id)
