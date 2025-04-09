from typing import List, Dict
from random import sample
from app.schemas.user import UserPrivate
from app.schemas.player import Player, PublicPlayer
from app.schemas.game import Game, GamePublic
from app.schemas.enum import FigType
from app.schemas.enum import GameColor
from app.crud.user import get_user_by_id
from .web_sockets import manager
from .room import get_room, room_private_to_public
from .fig_card import create_figure_cards_deck
from .player import create_player, get_new_mov_cards, destroy_used_fig_cards, initialize_hand, player_private_to_public
from .board import BOARD_DIM, create_board, detect_figures

games: Dict[str, Game] = {}

def create_game(room_id: str) -> Game:
    room = get_room(room_id)
    board = create_board()
    fige_deck, fig_deck = create_figure_cards_deck(1)
    fige_player_cards_number = len(fige_deck) // len(room.room_users)
    fig_player_cards_number = len(fig_deck) // len(room.room_users)
    player_colors = sample(list(GameColor), len(room.room_users))
    players = [create_player(user, fige_deck, fig_deck, fige_player_cards_number, fig_player_cards_number, player_colors.pop()) for user in room.room_users]
    players[0].in_turn = True
    game = Game(room=room, players=players, board=board)
    detect_figures(game.board, get_players_fig_types_to_detect(game))
    games[game.room.room_id] = game
    return game

def get_game(room_id: str) -> Game:
    return games.get(room_id)

def next_turn(room_id: str):
    game = get_game(room_id)
    users = game.room.room_users
    players = game.players
    for i, user in enumerate(users): 
        player = players[i]
        if player.in_turn:
            player.mov_cards = [mov_card for mov_card in player.mov_cards if not mov_card.is_used]
            get_new_mov_cards(player.mov_cards)
            destroy_used_fig_cards(player)
            if len([fig_card for fig_card in player.player_deck if fig_card.is_blocked]) == 0:
                initialize_hand(player.player_deck)
            next_player = players[(i + 1) % len(players)]
            player.in_turn = False
            next_player.in_turn = True
            break
    detect_figures(game.board, get_players_fig_types_to_detect(game))

def leave_game(user_id: str, room_id: str):
    game = get_game(room_id)
    user = get_user_by_id(user_id)
    player = get_player(game, user_id)
    if player.in_turn:
        next_turn(room_id)
    users = game.room.room_users
    players = game.players
    users.remove(user)
    players.remove(player) 
    detect_figures(game.board, get_players_fig_types_to_detect(game))

def delete_game(room_id: str):
    del games[room_id]            

def switch(user_id: str, room_id: str, mov_card_index: int, tile1_x: int, tile1_y: int, tile2_x: int, tile2_y: int):
    game = get_game(room_id)
    player = get_player(game, user_id)
    player.mov_cards[mov_card_index].is_used = True
    tile1 = game.board.tiles[tile1_x + tile1_y * BOARD_DIM]
    tile2 = game.board.tiles[tile2_x + tile2_y * BOARD_DIM]
    game.board.tiles[tile1_x + tile1_y * BOARD_DIM] = tile2
    game.board.tiles[tile2_x + tile2_y * BOARD_DIM] = tile1
    detect_figures(game.board, get_players_fig_types_to_detect(game))

def discard_figure(user_id: str, room_id: str, fig_card_index: int, tile_x: int, tile_y: int):
    game = get_game(room_id)
    player = get_player(game, user_id)
    fig_card = player.player_deck[fig_card_index]
    fig_card.is_used = True
    player.fig_cards_left = len([fig_card for fig_card in player.player_deck if not fig_card.is_used])
    fig_cards_left_in_hand = [fig_card for fig_card in player.player_deck if fig_card.in_hand and not fig_card.is_used]
    if len(fig_cards_left_in_hand) == 1:
        fig_cards_left_in_hand[0].is_blocked = False

    game.board.blocked_color = game.board.tiles[tile_x + tile_y * BOARD_DIM].color

    detect_figures(game.board, get_players_fig_types_to_detect(game))
    
def block_figure(room_id: str, playername: str, fig_card_index: int, tile_x: int, tile_y: int):
    game = get_game(room_id)
    player = get_player_by_name(game, playername)
    fig_card = player.fig_cards_in_hand[fig_card_index]
    fig_card.is_blocked = True
    game.board.blocked_color = game.board.tiles[tile_x + tile_y * BOARD_DIM].color

    detect_figures(game.board, get_players_fig_types_to_detect(game))
    
def game_private_to_public(game: Game, user: UserPrivate) -> GamePublic:
    public_room = room_private_to_public(game.room)
    my_player = next(player for player in game.players if player.username == user.username)
    other_players = [player_private_to_public(player) for player in game.players if player != my_player]
    board = game.board
    public_game = GamePublic(room=public_room, my_player=my_player, other_players=other_players, board=board)
    return public_game

def get_user_of_game(game: Game, user_id: str) -> UserPrivate:
    return next(user for user in game.room.room_users if user.user_id == user_id)

def get_player(game: Game, user_id: str) -> Player:
    user = get_user_of_game(game, user_id)
    return next(player for player in game.players if player.username == user.username)

def get_player_by_name(game: Game, playername: str) -> PublicPlayer:
    return next(player_private_to_public(player) for player in game.players if player.username == playername) 

def get_players_fig_types_to_detect(game: Game) -> List[FigType]:
    fig_types_to_detect = []
    for player in game.players:
        if player.in_turn:
            fig_types_to_detect += [fig_card.fig_type for fig_card in player.player_deck if fig_card.in_hand and not fig_card.is_used and not fig_card.is_blocked]
        else:
            if len([fig_card for fig_card in player.player_deck if fig_card.in_hand]) > 1:
                if len([fig_card for fig_card in player.player_deck if fig_card.in_hand and not fig_card.is_used and fig_card.is_blocked]) == 0:
                    fig_types_to_detect += [fig_card.fig_type for fig_card in player.player_deck if fig_card.in_hand]
    return fig_types_to_detect