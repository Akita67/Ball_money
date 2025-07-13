# obstacles.py

import pygame
import random
from settings import (
    OBSTACLE_COLOR, OBSTACLE_RADIUS,
    OBSTACLE_COLUMNS, OBSTACLE_ROWS,
    OBSTACLE_OFFSET_X, OBSTACLE_OFFSET_Y,
    OBSTACLE_SPACING_X, OBSTACLE_SPACING_Y
)

class Obstacles:
    def __init__(self):
        # Build a grid of obstacle rects centered on (x, y)
        self.obstacles = []
        extra = 0
        for row in range(OBSTACLE_ROWS):
            for col in range(OBSTACLE_COLUMNS):
                extra = 0
                if(row%2==0):
                    extra = 50
                x = OBSTACLE_OFFSET_X + col * OBSTACLE_SPACING_X + extra
                y = OBSTACLE_OFFSET_Y + row * OBSTACLE_SPACING_Y
                rect = pygame.Rect(
                    x - OBSTACLE_RADIUS,
                    y - OBSTACLE_RADIUS,
                    OBSTACLE_RADIUS * 2,
                    OBSTACLE_RADIUS * 2
                )
                self.obstacles.append(rect)

    def draw(self, surface):
        for rect in self.obstacles:
            center = (rect.x + OBSTACLE_RADIUS, rect.y + OBSTACLE_RADIUS)
            pygame.draw.circle(surface, OBSTACLE_COLOR, center, OBSTACLE_RADIUS)

    def check_collision(self, ball):
        """
        If the ball collides with any obstacle, invert its vertical velocity.
        Returns True if a collision occurred.
        """
        value = random.uniform(-0.1, 0.1)
        ball_rect = ball.get_rect()
        for rect in self.obstacles:
            if ball_rect.colliderect(rect):
                # invert vertical velocity
                ball.vy = -ball.vy / 1.1
                # push ball horizontally away from obstacle center
                obstacle_cx = rect.x + OBSTACLE_RADIUS

                if ball.x < obstacle_cx:# bounce left
                    ball.vx = -abs(ball.vx)
                else: # bounce right
                    ball.vx = abs(ball.vx)

                return True
        return False
