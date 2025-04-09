from app.schemas.board import Board
from app.schemas.tile import Tile
from app.schemas.enum import TileColor, FigType
from .figure_detector import detect_figure, clear_detector
from typing import List
from random import shuffle

BOARD_DIM = 6

def create_board() -> Board:
    tile_colors = get_color_list()
    tiles = [None for _ in range(BOARD_DIM ** 2)]
    for i in range(BOARD_DIM ** 2):
        tiles[i] = Tile(color=tile_colors.pop(), figure=FigType.NONE)
    return Board(tiles=tiles, blocked_color=TileColor.NONE)

def get_color_list() -> List[TileColor]:
    colors = [TileColor.RED, TileColor.YELLOW, TileColor.GREEN, TileColor.BLUE]
    count_per_color = BOARD_DIM ** 2 // len(colors)
    color_list = colors * count_per_color
    shuffle(color_list)
    return color_list

def detect_figures(board: Board, fig_types: List[FigType]):
    clear_detector(board)
    for y in range(BOARD_DIM):
        for x in range(BOARD_DIM):
            for fig_type in fig_types:
                detect_figure(board, x, y, fig_type)
