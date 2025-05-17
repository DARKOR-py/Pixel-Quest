import pygame as pg


class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def return_rect(self):
        return self.rect
