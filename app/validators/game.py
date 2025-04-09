from app.crud.user import get_user_by_id
from app.services.game import get_player, get_player_by_name, get_game 
from app.services.board import BOARD_DIM
from app.services.mov_card import get_posible_target_positions
from fastapi import HTTPException, status
from typing import List

def check_game_exists(room_id):
    game = get_game(room_id)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Game not found")
    
def check_user_in_game(user_id: str, room_id: str):
    user = get_user_by_id(user_id)
    game = get_game(room_id)
    if not user in game.room.room_users:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User is not in the game")

def check_player_has_turn(user_id: str, room_id: str):
    game = get_game(room_id)
    player = get_player(game, user_id)
    if not player.in_turn:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Player has no turn")

def check_valid_range_board(coordinates: List[int]):
    for coordinate in coordinates:
        if not 0 <= coordinate <= BOARD_DIM: 
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Tile position out of range")
    
def check_mov_card(user_id: str, room_id: str, mov_card_index: int):
    game = get_game(room_id)
    player = get_player(game, user_id)
    if not 0 <= mov_card_index < len(player.mov_cards):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid mov card index")
    mov_card = player.mov_cards[mov_card_index]
    if mov_card.is_used:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Mov card is already used")

def check_valid_switch(user_id: str, room_id: str, mov_card_index: int, tile1_x: int, tile1_y: int, tile2_x: int, tile2_y: int):
    game = get_game(room_id)
    player = get_player(game, user_id)
    mov_type = player.mov_cards[mov_card_index].mov_type
    target_position = (tile2_x, tile2_y)
    if target_position not in get_posible_target_positions(mov_type, tile1_x, tile1_y):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid switch")

def check_fig_card(user_id: str, room_id: str, fig_card_index: int):
    game = get_game(room_id)
    player = get_player(game, user_id)
    if not 0 <= fig_card_index < len([fig_card for fig_card in player.player_deck if fig_card.in_hand]):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid fig card index")
    fig_card = player.player_deck[fig_card_index]
    if fig_card.is_used:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Fig card is already used")
    if fig_card.is_blocked:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Fig card is blocked")
    
def check_valid_figure_discard(user_id: str, room_id: str, fig_card_index: int, tile_x: int, tile_y: int):
    game = get_game(room_id)
    player = get_player(game, user_id)
    fig_type = player.player_deck[fig_card_index].fig_type
    tile = game.board.tiles[tile_x + tile_y * BOARD_DIM]
    if tile.figure != fig_type:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid figure")
    
def check_block_other_player(user_id: str, room_id: str, playername: str):
    game = get_game(room_id)
    player1 = get_player(game, user_id)
    player2 = get_player_by_name(game, playername)
    if player1.username == player2.username:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="It is not other player")
    if len([fig_card for fig_card in player2.fig_cards_in_hand if fig_card.is_blocked]):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Player already has a blocked card")
    if len(player2.fig_cards_in_hand) == 1:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Player only has a card")

def check_other_player_fig_card(room_id: str, playername: str, fig_card_index: int):
    game = get_game(room_id)
    player = get_player_by_name(game, playername)
    if not 0 <= fig_card_index < len([fig_card for fig_card in player.fig_cards_in_hand]):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid fig card index")
    fig_card = player.fig_cards_in_hand[fig_card_index]
    if fig_card.is_used:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Fig card is already used")
    if fig_card.is_blocked:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Fig card is blocked")
    
def check_valid_figure_block(room_id: str, playername: str, fig_card_index: int, tile_x: int, tile_y: int):
    game = get_game(room_id)
    player = get_player_by_name(game, playername)
    fig_type = player.fig_cards_in_hand[fig_card_index].fig_type
    tile = game.board.tiles[tile_x + tile_y * BOARD_DIM]
    if tile.figure != fig_type:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid figure")
