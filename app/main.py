from fastapi import FastAPI
from .api import web_sockets, user, room, game

app = FastAPI()

app.include_router(web_sockets.router)
app.include_router(user.router)
app.include_router(room.router)
app.include_router(game.router)