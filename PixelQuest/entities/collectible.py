import pygame as pg
import math


class Collectible:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.base_y = y
        self.radius = r
        self.isCollected = False
        self.isAnimationDone = False
        self.collect_start_time = 0
        self.rect = pg.Rect(self.x - int(r/2), self.y - int(r/2), r, r)

        self.collect_velocity = -8
        self.gravity = 1

    def return_rect(self):
        return self.rect

    def return_circle_info(self):
        return self.x, self.y, self.radius

    def start_animation(self):
        self.collect_start_time = pg.time.get_ticks()

    def animation(self):
        if not self.isCollected:
            speed = 2
            extent = 5
            time = pg.time.get_ticks() / 1000
            offset = math.sin(time * speed) * extent
            self.y = self.base_y + offset

        elif self.isCollected and not self.isAnimationDone:
            self.y += self.collect_velocity
            self.collect_velocity += self.gravity

            if self.y > self.base_y + 10:
                self.isAnimationDone = True
