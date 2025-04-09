from fastapi import APIRouter, status
from app.schemas.game import GamePublic
from app.crud.user import get_user_by_id
from app.validators.room import check_room_exists, check_room_owner, check_user_in_room
from app.validators.user import check_user_exists
from app.validators.game import check_block_other_player, check_fig_card, check_game_exists,  \
    check_mov_card, check_block_other_player, check_other_player_fig_card, check_user_in_game, \
    check_player_has_turn, check_valid_figure_block, check_valid_figure_discard, \
    check_valid_range_board, check_valid_switch
from app.services.web_sockets import manager
from app.services.room import delete_room
from app.services.game import block_figure, create_game, delete_game, discard_figure, get_game, next_turn, leave_game, switch, game_private_to_public
from app.services.timer import start_game_timer, cancel_game_timer

router = APIRouter(prefix="/game", tags=["Game"])

@router.post("/{user_id}/{room_id}", response_model=GamePublic, status_code=status.HTTP_201_CREATED)
async def create_game_endpoint(user_id: str, room_id: str):
    check_user_exists(user_id)
    check_room_exists(room_id)
    check_user_in_room(user_id, room_id)
    check_room_owner(user_id, room_id)

    game = create_game(room_id)
    delete_room(room_id)
    await manager.broadcast_to_room(room_id, "game_started")
    await start_game_timer(room_id)
    return game_private_to_public(game, get_user_by_id(user_id))

@router.get("/{user_id}/{room_id}", response_model=GamePublic)
def get_room_endpoint(user_id: str, room_id: str):
    check_user_exists(user_id)
    check_game_exists(room_id)
    check_user_in_game(user_id, room_id)

    return game_private_to_public(get_game(room_id), get_user_by_id(user_id))

@router.put("/leave/{user_id}/{room_id}", response_model=str)
async def leave_game_endpoint(user_id: str, room_id: str):
    check_user_exists(user_id)
    check_game_exists(room_id)
    check_user_in_game(user_id, room_id)
   
    leave_game(user_id, room_id)
    await manager.broadcast_to_room(room_id, f"player_left: {get_user_by_id(user_id).username}")
    await manager.leave_room_broadcast(user_id, room_id)
    if len(get_game(room_id).room.room_users) == 0:
        await cancel_game_timer(room_id)
        delete_game(room_id)

    return "player_left"


@router.put("/next_turn/{user_id}/{room_id}", response_model=str)
async def leave_game_endpoint(user_id: str, room_id: str):
    check_user_exists(user_id)
    check_game_exists(room_id)
    check_user_in_game(user_id, room_id)
    check_player_has_turn(user_id, room_id)

    next_turn(room_id)
    await manager.broadcast_to_room(room_id, f"next_turn")
    await start_game_timer(room_id)

    return "next_turn"

@router.put("/switch/{user_id}/{room_id}/{mov_card_index}/{tile1_x}/{tile1_y}/{tile2_x}/{tile2_y}", response_model=str)
async def leave_game_endpoint(user_id: str, room_id: str, mov_card_index: int, tile1_x: int, tile1_y: int, tile2_x: int, tile2_y: int):
    check_user_exists(user_id)
    check_game_exists(room_id)
    check_user_in_game(user_id, room_id)
    check_player_has_turn(user_id, room_id)
    check_valid_range_board([tile1_x, tile1_y, tile2_x, tile2_y])
    check_mov_card(user_id, room_id, mov_card_index)
    check_valid_switch(user_id, room_id, mov_card_index, tile1_x, tile1_y, tile2_x, tile2_y)

    switch(user_id, room_id, mov_card_index, tile1_x, tile1_y, tile2_x, tile2_y)
    await manager.broadcast_to_room(room_id, f"switch: {mov_card_index}, {tile1_x}, {tile1_y}, {tile2_x}, {tile2_y}")
    
    return "switch"

@router.put("/figure/discard/{user_id}/{room_id}/{fig_card_index}/{tile_x}/{tile_y}", response_model=str)
async def leave_game_endpoint(user_id: str, room_id: str, fig_card_index: int, tile_x: int, tile_y: int):
    check_user_exists(user_id)
    check_game_exists(room_id)
    check_user_in_game(user_id, room_id)
    check_player_has_turn(user_id, room_id)
    check_valid_range_board([tile_x, tile_y])
    check_fig_card(user_id, room_id, fig_card_index)
    check_valid_figure_discard(user_id, room_id, fig_card_index, tile_x, tile_y)

    discard_figure(user_id, room_id, fig_card_index, tile_x, tile_y)
    await manager.broadcast_to_room(room_id, f"figure_discard: {fig_card_index}")
    
    return "figure_discard"

@router.put("/figure/block/{user_id}/{room_id}/{playername}/{fig_card_index}/{tile_x}/{tile_y}", response_model=str)
async def leave_game_endpoint(user_id: str, room_id: str, playername: str, fig_card_index: int, tile_x: int, tile_y: int):
    check_user_exists(user_id)
    check_game_exists(room_id)
    check_user_in_game(user_id, room_id)
    check_player_has_turn(user_id, room_id)
    check_block_other_player(user_id, room_id, playername)
    check_valid_range_board([tile_x, tile_y])
    check_other_player_fig_card(room_id, playername, fig_card_index)
    check_valid_figure_block(room_id, playername, fig_card_index, tile_x, tile_y)

    block_figure(room_id, playername, fig_card_index, tile_x, tile_y)
    await manager.broadcast_to_room(room_id, f"figure_block")
    
    return "figure_block"