from pydantic import BaseModel
from .enum import TileColor
from .fig_card import FigType

class Tile(BaseModel):
    color: 'TileColor'
    figure: 'FigType'