from app.schemas.fig_card import FigCard
from app.schemas.enum import FigType
from typing import List, Tuple
from random import choice

def create_figure_cards_deck(decks_amount: int) -> Tuple[List[FigCard], List[FigCard]]:
    """Crea los mazos de cartas FIGE y FIG, mezclando el mazo de FIG."""
    fige_types, fig_types = get_card_types(decks_amount)
    fige_cards_deck = build_deck(fige_types)
    fig_cards_deck = build_deck(fig_types)
    return fige_cards_deck, fig_cards_deck

def build_deck(card_types: List[FigType]) -> List[FigCard]:
    """Construye un mazo de cartas dado una lista de tipos de FigType."""
    return [FigCard(fig_type=fig_type, in_hand=False, is_blocked=False, is_used=False) for fig_type in card_types]

def get_card_types(decks_amount: int) -> Tuple[List[FigType], List[FigType]]:
    """Obtiene los tipos de FIGE y FIG, multiplicados por la cantidad de mazos."""
    fige_types = [FigType.FIGE_1, FigType.FIGE_2, FigType.FIGE_3, FigType.FIGE_4, FigType.FIGE_5, FigType.FIGE_6, FigType.FIGE_7]
    fig_types = [fig_type for fig_type in FigType if fig_type not in fige_types and fig_type != FigType.NONE]
    
    return fige_types * decks_amount, fig_types * decks_amount
