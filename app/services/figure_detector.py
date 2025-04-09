from app.schemas.board import Board
from app.schemas.enum import FigType
from typing import List, Tuple

BOARD_DIM = 6

def detect_figure(board: Board, origin_x: int, origin_y: int, fig_type: FigType):
    """Detecta la figura del tipo indicado alrededor del las coordenadas de origen"""
    if not board.blocked_color == board.tiles[origin_x + origin_y * BOARD_DIM].color:
        all_rots_fig_tiles_offsets = get_all_rots_fig_tiles_offsets(fig_type)
        all_rots_border_tiles_offsets = get_all_rots_border_tiles_offsets(all_rots_fig_tiles_offsets)
        find_figure(board, origin_x, origin_y, fig_type, all_rots_fig_tiles_offsets, all_rots_border_tiles_offsets)


def find_figure(board: Board, origin_x: int, origin_y: int, fig_type: FigType, 
                all_rots_fig_tiles_offsets: List[List[Tuple[int, int]]], 
                all_rots_border_tiles_offsets: List[List[Tuple[int, int]]]):
    """verifica si los bordes para formar la figura son validos, y si lo son intenta formarla"""
    
    if not is_valid_pos(origin_x, origin_y):
        return
    
    finding_for_color = board.tiles[origin_x + origin_y * BOARD_DIM].color
    fig_tiles_positions: List[int] = []

    for rot, rot_fig_tiles_offsets in enumerate(all_rots_fig_tiles_offsets):
        fig_tiles_positions.clear()
        is_valid_border = True  

        for border_tiles_offset in all_rots_border_tiles_offsets[rot]:
            border_x = origin_x + border_tiles_offset[0]
            border_y = origin_y + border_tiles_offset[1]
            if is_valid_pos(border_x, border_y):
                border_pos = border_x + border_y * BOARD_DIM
                if board.tiles[border_pos].color == finding_for_color:
                    is_valid_border = False
                    break

        if is_valid_border:
            for fig_tiles_offsets in rot_fig_tiles_offsets:
                x = origin_x + fig_tiles_offsets[0]
                y = origin_y + fig_tiles_offsets[1]
                if not is_valid_pos(x, y):
                    fig_tiles_positions.clear()
                    break
                else:
                    tile_pos = x + y * BOARD_DIM
                    if board.tiles[tile_pos].color == finding_for_color:
                        fig_tiles_positions.append(tile_pos)
                    else:
                        fig_tiles_positions.clear()
                        break
        
        if fig_tiles_positions:
            for fig_tile_position in fig_tiles_positions:
                board.tiles[fig_tile_position].figure = fig_type
            return

def is_valid_pos(x: int, y: int) -> bool:
    return 0 <= x < BOARD_DIM and 0 <= y < BOARD_DIM

def clear_detector(board: Board):
    for tile in board.tiles:
        tile.figure = FigType.NONE

def get_all_rots_fig_tiles_offsets(fig_type: FigType) -> List[List[Tuple[int, int]]]:
    """Obtiene la figura en cada rotacion"""
    match fig_type:
        case FigType.FIGE_1:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, 0), (0, 0), (0, -1), (1, -1)])
        case FigType.FIGE_2:
            all_rots_fig_tiles_offsets = generate_rotations([(0, 0), (1, 0), (0, -1), (1, -1)])
        case FigType.FIGE_3:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, -1), (0, -1), (0, 0), (1, 0)])
        case FigType.FIGE_4:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, 0), (0, 0), (1, 0), (0, -1)])
        case FigType.FIGE_5:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -1), (0, 0), (0, 1), (-1, 1)])
        case FigType.FIGE_6:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, 0), (0, 0), (1, 0), (2, 0)])
        case FigType.FIGE_7:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -1), (0, 0), (0, 1), (1, 1)])
        case FigType.FIG_01:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, 0), (0, 0), (1, 0), (0, -1), (0, -2)])
        case FigType.FIG_02:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, -1), (0, -1), (0, 0), (1, 0), (2, 0)])
        case FigType.FIG_03:
            all_rots_fig_tiles_offsets = generate_rotations([(1, -1), (0, -1), (0, 0), (-1, 0), (-2, 0)])
        case FigType.FIG_04:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, -1), (-1, 0), (0, 0), (0, 1), (1, 1)])
        case FigType.FIG_05:
            all_rots_fig_tiles_offsets = generate_rotations([(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)])
        case FigType.FIG_06:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -2), (0, -1), (0, 0), (1, 0), (2, 0)])
        case FigType.FIG_07:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -2), (0, -1), (0, 0), (0, 1), (-1, 1)])
        case FigType.FIG_08:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -2), (0, -1), (0, 0), (0, 1), (1, 1)])
        case FigType.FIG_09:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -1), (1, 0), (0, 0), (-1, 0), (-1, 1)])
        case FigType.FIG_10:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, -1), (0, -1), (0, 0), (0, 1), (1, 1)])
        case FigType.FIG_11:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -1), (1, 0), (0, 0), (-1, 0), (1, 1)])
        case FigType.FIG_12:
            all_rots_fig_tiles_offsets = generate_rotations([(1, -1), (0, -1), (0, 0), (0, 1), (-1, 1)])
        case FigType.FIG_13:
            all_rots_fig_tiles_offsets = generate_rotations([(-2, 0), (-1, 0), (0, 0), (1, 0), (0, 1)])
        case FigType.FIG_14:
            all_rots_fig_tiles_offsets = generate_rotations([(-2, 0), (-1, 0), (0, 0), (1, 0), (0, -1)])
        case FigType.FIG_15:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -1), (1, -1), (1, 0), (0, 0), (-1, 0)])
        case FigType.FIG_16:
            all_rots_fig_tiles_offsets = generate_rotations([(1, -1), (0, -1), (0, 0), (0, 1), (1, 1)])
        case FigType.FIG_17:
            all_rots_fig_tiles_offsets = generate_rotations([(-1, 0), (0, 0), (1, 0), (0, -1), (0, 1)])
        case FigType.FIG_18:
            all_rots_fig_tiles_offsets = generate_rotations([(0, -1), (1, -1), (1, 0), (0, 0), (-1, -1)])
    return all_rots_fig_tiles_offsets

def generate_rotations(figure: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    """Genera hasta 4 rotaciones unicas de la figura."""
    rotations = [figure]    
    new_rotation1 = [(y, -x) for x, y in figure]
    if new_rotation1 not in rotations:
        rotations.append(new_rotation1)
    new_rotation2 = [(-x, -y) for x, y in figure]
    if new_rotation2 not in rotations:
        rotations.append(new_rotation2)
    new_rotation3 = [(-y, x) for x, y in figure]
    if new_rotation3 not in rotations:
        rotations.append(new_rotation3)
    return rotations


def get_all_rots_border_tiles_offsets(all_rots_fig_tiles_offsets: List[List[Tuple[int, int]]]):
    """Obtiene los bordes de la figura en cada rotacion"""
    all_rots_border_tiles_offsets: List[List[Tuple[int, int]]] = []
    for rot_fig_tiles_offsets in all_rots_fig_tiles_offsets:
        rot_border_tiles_offsets: List[Tuple[int, int]] = []
        for vector in rot_fig_tiles_offsets:
            borders = [
                (vector[0] + 1, vector[1]),
                (vector[0] - 1, vector[1]),
                (vector[0], vector[1] + 1),
                (vector[0], vector[1] - 1)]
            for border in borders:
                if border not in rot_fig_tiles_offsets and border not in rot_border_tiles_offsets:
                    rot_border_tiles_offsets.append(border)
        all_rots_border_tiles_offsets.append(rot_border_tiles_offsets)
    return all_rots_border_tiles_offsets