from app.schemas.user import UserPrivate
from app.schemas.fig_card import FigCard
from app.schemas.mov_card import MovCard
from app.schemas.player import Player, PublicPlayer
from app.schemas.enum import GameColor, MovType
from typing import List
from random import shuffle, choice

def create_player(user: UserPrivate, fige_deck: List[FigCard], fig_deck: List[FigCard], fige_cards_number: int, fig_cards_number: int, player_color: GameColor) -> Player:
    mov_cards = get_new_mov_cards([])
    fige_cards = draw_cards(fige_deck, fige_cards_number)
    fig_cards = draw_cards(fig_deck, fig_cards_number)
    player_deck: List[FigCard] = fige_cards + fig_cards
    in_turn = False
    shuffle(player_deck)
    initialize_hand(player_deck)
    fig_cards_left = len([fig_card for fig_card in player_deck if not fig_card.is_used])
    return Player(username=user.username, mov_cards=mov_cards, player_deck=player_deck, fig_cards_left=fig_cards_left, in_turn=in_turn, player_color=player_color)

def draw_cards(deck: List[FigCard], count: int) -> List[FigCard]:
    """Extrae count cartas de deck."""
    return [deck.pop() for _ in range(count)]

def initialize_hand(player_deck: List[FigCard]) -> None:
    """Marca las primeras tres cartas del mazo como en mano."""
    for i in range(min(3, len(player_deck))):
        player_deck[i].in_hand = True

def player_private_to_public(player: Player) -> PublicPlayer:
    username = player.username
    fig_cards_in_hand = [fig_card for fig_card in player.player_deck if fig_card.in_hand]
    in_turn = player.in_turn
    player_color = player.player_color
    fig_cards_left = player.fig_cards_left
    return PublicPlayer(username=username, fig_cards_in_hand=fig_cards_in_hand, fig_cards_left=fig_cards_left, in_turn=in_turn, player_color=player_color)

def get_new_mov_cards(mov_cards: List[MovCard]) -> List[MovCard]:
    new_mov_cards = mov_cards
    while len(new_mov_cards) < 3:
        new_mov_cards.append(MovCard(mov_type=choice(list(MovType)), is_used=False))
    return new_mov_cards

def destroy_used_fig_cards(player: Player):
    player.player_deck = [fig_card for fig_card in player.player_deck if not fig_card.is_used]