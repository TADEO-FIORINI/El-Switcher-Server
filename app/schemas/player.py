from pydantic import BaseModel
from typing import List
from .mov_card import MovCard
from .fig_card import FigCard
from .enum import GameColor

class Player(BaseModel):
    username: str
    mov_cards: List[MovCard]
    player_deck: List[FigCard]
    fig_cards_left: int
    in_turn: bool
    player_color: GameColor

class PublicPlayer(BaseModel):
    username: str
    fig_cards_in_hand: List[FigCard]
    fig_cards_left: int
    in_turn: bool
    player_color: GameColor