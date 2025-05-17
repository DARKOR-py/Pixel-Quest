import pygame as pg
from settings import GRAVITY, FRICTION


class Player:
    def __init__(self, w, h):
        self.respawn_point = [50, 10]
        self.x, self.y = self.respawn_point
        self.width = w
        self.height = h

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.isColliding = False
        self.canJump = False
        self.isDead = False
        self.speedY = 0
        self.speedX = 0
        self.acceleration_speed = 5
        self.jump_height = 10

    def move_y(self):
        if not self.isColliding:
            self.speedY += GRAVITY
        self.y += self.speedY
        self.rect.y = self.y

    def apply_friction(self):
        self.speedX *= FRICTION
        if abs(self.speedX) < 0.1:
            self.speedX = 0
        self.x += self.speedX
        self.rect.x = self.x

    def move_x(self, step):
        self.speedX += step

    def return_rect(self):
        return self.rect

    def on_death(self):
        self.isDead = True

        self.x, self.y = self.respawn_point

        self.isDead = False
