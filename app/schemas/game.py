from pydantic import BaseModel
from typing import List
from .room import RoomPrivate, RoomPublic
from .player import Player, PublicPlayer
from .board import Board

class Game(BaseModel):
    room: RoomPrivate
    players: List[Player]
    board: Board

class GamePublic(BaseModel):
    room: RoomPublic
    my_player: Player
    other_players: List[PublicPlayer]
    board: Board