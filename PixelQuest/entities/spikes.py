import pygame as pg


class Spike:
    def __init__(self, x, y, w, h):
        self.width = w
        self.height = h
        self.x, self.y = x, y
        self.hitbox_len = 10

    def return_poly_info(self):
        return [
            (self.x, self.y + self.height),
            (self.x + self.width / 2, self.y),
            (self.x + self.width, self.y + self.height)
        ]

    def return_rect(self, hitbox_len):
        x_offset = (self.width - hitbox_len) / 2
        hitbox_x = self.x + x_offset

        hitbox_height = self.height * (hitbox_len / self.width)
        hitbox_y = self.y + self.height - hitbox_height

        return pg.Rect(hitbox_x, hitbox_y, hitbox_len, hitbox_height)

