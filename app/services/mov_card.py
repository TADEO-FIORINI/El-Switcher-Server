from app.schemas.enum import MovType
from typing import List, Tuple
from random import choice
from .board import BOARD_DIM

def get_posible_target_positions(mov_type: MovType, origin_tile_x: int, origin_tile_y: int) -> List[Tuple[int, int]]:
    """Devuelve las posiciones posibles según el tipo de movimiento"""
    offsets = get_target_offsets(mov_type, origin_tile_x, origin_tile_y)
    if mov_type != MovType.MOV_7:
        return get_valid_positions(generate_positions(origin_tile_x, origin_tile_y, offsets))
    else:
        return generate_mov7_valid_positions(origin_tile_x, origin_tile_y)

def generate_positions(origin_x: int, origin_y: int, offsets: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Genera nuevas posiciones basadas en desplazamientos dados"""
    return [(origin_x + dx, origin_y + dy) for dx, dy in offsets]

def get_valid_positions(targets: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Filtra posiciones fuera del tablero"""
    return [pos for pos in targets if 0 <= pos[0] <= BOARD_DIM and 0 <= pos[1] <= BOARD_DIM]

def generate_mov7_valid_positions(origin_tile_x: int, origin_tile_y: int) -> List[Tuple[int, int]]:
    return [(0, origin_tile_y), (5, origin_tile_y), (origin_tile_x, 0), (origin_tile_x, 5)]

def get_target_offsets(mov_type: MovType, origin_tile_x: int, origin_tile_y: int) -> List[Tuple[int, int]]:
    """Obtiene los posibles offsets de los target de un movimiento"""
    match mov_type:
        case MovType.MOV_1:
            offsets = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        case MovType.MOV_2:
            offsets = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        case MovType.MOV_3:
            offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        case MovType.MOV_4:
            offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        case MovType.MOV_5:
            offsets = [(1, -2), (-1, 2), (-2, -1), (2, 1)]
        case MovType.MOV_6:
            offsets = [(1, 2), (-1, -2), (2, -1), (-2, 1)]
        case MovType.MOV_7:
            offsets = [(0, origin_tile_y), (5, origin_tile_y), (origin_tile_x, 0), (origin_tile_x, 5)]
        case _:
            return []
    return offsets