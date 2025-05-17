import pygame as pg
from settings import SCREEN

pg.init()


def rect(color, rect):
    surface = pg.Surface(SCREEN.get_size(), pg.SRCALPHA)
    pg.draw.rect(surface, color, rect)
    SCREEN.blit(surface, (0, 0))


def circle(color, circle_info):
    surface = pg.Surface(SCREEN.get_size(), pg.SRCALPHA)
    pg.draw.circle(surface, color, (circle_info[0], circle_info[1]), circle_info[2])
    SCREEN.blit(surface, (0, 0))


def polygon(color, points):
    surface = pg.Surface(SCREEN.get_size(), pg.SRCALPHA)
    pg.draw.polygon(surface, color, points)
    SCREEN.blit(surface, (0, 0))


default_font = pg.font.SysFont("Arial", 30)


def font(content, color, pos):
    text_surface = default_font.render(content, True, color)
    SCREEN.blit(text_surface, pos)