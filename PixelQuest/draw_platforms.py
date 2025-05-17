import pygame as pg
from settings import SCREEN, PLATFORM_SPRITE_MAP


def get_platform_sprite(x, y, level):
    max_y = len(level)
    max_x = len(level[0]) if max_y > 0 else 0

    def is_platform(x, y):
        return 0 <= x < max_x and 0 <= y < max_y and level[y][x] == '#'

    left = is_platform(x - 1, y)
    right = is_platform(x + 1, y)
    up = is_platform(x, y - 1)
    down = is_platform(x, y + 1)

    return up, down, left, right


def draw_platform(x, y, level):
    connections = get_platform_sprite(x, y, level)
    print(connections)
    platform_data = PLATFORM_SPRITE_MAP.get(connections)
    print(platform_data)

    platform_surface, orientation = platform_data

    if orientation == 'h':
        pass  # horizontal, no rotation
    elif orientation == 'v':
        platform_surface = pg.transform.rotate(platform_surface, 90)
    elif orientation == 'r':
        platform_surface = pg.transform.rotate(platform_surface, 0)
    elif orientation == 'd':
        platform_surface = pg.transform.rotate(platform_surface, 90)
    elif orientation == 'l':
        platform_surface = pg.transform.rotate(platform_surface, 180)
    elif orientation == 'u':
        platform_surface = pg.transform.rotate(platform_surface, 270)

    SCREEN.blit(platform_surface, (x, y))