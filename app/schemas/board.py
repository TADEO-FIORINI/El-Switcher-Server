from pydantic import BaseModel
from typing import List
from .tile import Tile
from .fig_card import FigType
from .enum import TileColor

class Board(BaseModel):
    blocked_color: TileColor
    tiles: List[Tile]

class Tile(BaseModel):
    color: TileColor
    figure: FigType