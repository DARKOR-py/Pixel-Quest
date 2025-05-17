import pygame as pg
import math


class Interactible:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.isInteracted = False

    def return_rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)


class Checkpoint(Interactible):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.isOn = False

    def return_diamond_points(self):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        return [
            (cx, self.y),  # top
            (self.x + self.width, cy),  # right
            (cx, self.y + self.height),  # bottom
            (self.x, cy)  # left
        ]


class EndFlag(Interactible):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.isReached = False


class JumpOrb(Interactible):
    def __init__(self, x, y, r):
        self.radius = r
        self.base_radius = r
        self.activated = False
        self.activation_time = 0
        self.tap_duration = 200     # ms
        self.animation_radius = r*2
        self.x = x
        self.y = y
        super().__init__(x, y, r, r)

    def animation(self):
        current_time = pg.time.get_ticks()

        if self.activated:
            elapsed = current_time - self.activation_time
            if elapsed < self.tap_duration:
                scale = 1.2 - (elapsed / self.tap_duration) * 0.4
                self.radius = self.base_radius * scale
                self.animation_radius = (self.base_radius*2) * scale
            else:
                self.radius = self.base_radius
                self.animation_radius = self.base_radius * 2
                self.activated = False
        else:
            time = current_time / 1000
            scale = 1 + 0.1 * math.sin(time * 3)
            self.animation_radius = self.base_radius*2 * scale

    def activate(self):
        self.activated = True
        self.activation_time = pg.time.get_ticks()

    def return_circle_info(self):
        return self.x, self.y, self.radius

    def animation_circle(self):
        return self.x, self.y, self.animation_radius

    def return_hitbox(self, size):
        return pg.Rect(self.x - size//2, self.y - size//2, size, size)