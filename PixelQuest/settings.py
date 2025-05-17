import pygame as pg

ASPECT_RATIO = [16, 9]
TILE_SIZE = 32
COEFICIENT = 2
SCREEN_WIDTH = ASPECT_RATIO[0] * TILE_SIZE * COEFICIENT
SCREEN_HEIGHT = ASPECT_RATIO[1] * TILE_SIZE * COEFICIENT
FPS = 60
PLAYER_WIDTH = TILE_SIZE
PLAYER_HEIGHT = TILE_SIZE
GRAVITY = 1
FRICTION = 0.8

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

MAP_FILENAME = "map.json"

GAME_STATE = "menu"
# game states : menu, pause, options...


def load(path):
    return pg.image.load(path)


PLATFORM_SPRITE_MAP = {
    # Connexions : (up, down, left, right)
    (False, False, False, False): [load("assets/images/crate0.png"), None],  # Solo
    (False, False, True, False):  [load("assets/images/crate1.png"), 'l'],  # 1 connection
    (True, False, False, False):  [load("assets/images/crate1.png"), 'u'],  # 1 connection
    (False, True, False, False):  [load("assets/images/crate1.png"), 'd'],  # 1 connection
    (False, False, False, True):  [load("assets/images/crate1.png"), 'r'],  # 1 connection
    (False, False, True, True):  [load("assets/images/crate2.png"), 'h'],  # 2 connections, linear horizontal
    (True, True, False, False):  [load("assets/images/crate2.png"), 'v'],  # 2 connections, linear vertical
    (True, False, False, True):   [load("assets/images/crate3.png"), 'r'],  # 2 connections, L right
    (False, True, False, True):   [load("assets/images/crate3.png"), 'd'],  # 2 connections, L down
    (False, True, True, False):   [load("assets/images/crate3.png"), 'l'],  # 2 connections, L left
    (True, False, True, False):   [load("assets/images/crate3.png"), 'u'],  # 2 connections, L up
    (False, True, False, True):   [load("assets/images/crate4.png"), 'r'],  # 2 connections, anti L right
    (False, True, True, False):   [load("assets/images/crate4.png"), 'd'],  # 2 connections, anti L down
    (True, False, True, False):   [load("assets/images/crate4.png"), 'l'],  # 2 connections, anti L left
    (True, False, True, False):   [load("assets/images/crate4.png"), 'u'],  # 2 connections, anti L up
    (True, True, False, True):    [load("assets/images/crate5.png"), 'r'],  # 3 connections, t right
    (False, True, True, True):    [load("assets/images/crate5.png"), 'd'],  # 3 connections, t down
    (True, True, True, False):    [load("assets/images/crate5.png"), 'l'],  # 3 connections, t left
    (True, False, True, True):    [load("assets/images/crate5.png"), 'u'],  # 3 connections, t up
    (True, False, True, True):    [load("assets/images/crate6.png"), None]    # all four
}
