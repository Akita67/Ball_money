import pygame
import random
from settings import BALL_RADIUS, BALL_COLOR, GRAVITY, BALL_INIT_VX_MIN, BALL_INIT_VX_MAX, COLOR_RANDOM

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.vx = random.uniform(BALL_INIT_VX_MIN, BALL_INIT_VX_MAX)
        self.radius = BALL_RADIUS

    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        self.y += self.vy
        self.x += self.vx

    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, (int(self.x), int(self.y)), self.radius)

    def off_screen(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        # For collision detection
        return pygame.Rect(
            int(self.x) - self.radius,
            int(self.y) - self.radius,
            self.radius * 2,
            self.radius * 2
        )