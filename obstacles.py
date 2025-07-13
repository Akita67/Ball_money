# obstacles.py

import pygame
import random
import time

from settings import (
    OBSTACLE_COLOR, OBSTACLE_RADIUS,
    OBSTACLE_COLUMNS, OBSTACLE_ROWS,
    OBSTACLE_OFFSET_X, OBSTACLE_OFFSET_Y,
    OBSTACLE_SPACING_X, OBSTACLE_SPACING_Y,
    SCREEN_WIDTH, SCREEN_HEIGHT,
)

GLOW_DURATION = 150  # milliseconds
GLOW_COLOR = (255, 255, 255)  # white halo

class Obstacles:
    def __init__(self):

        wall_thickness = 10
        self.left_wall = pygame.Rect(100, 0, wall_thickness, SCREEN_HEIGHT)
        self.right_wall = pygame.Rect(SCREEN_WIDTH - ( wall_thickness + 40 ), 0, wall_thickness, SCREEN_HEIGHT)
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
                self.obstacles.append({
                    "rect": rect,
                    "glow_until": 0  # timestamp in ms
                })

    def draw(self, surface):
        now = pygame.time.get_ticks()
        value = random.uniform(0, 255)
        value1 = random.uniform(0, 255)
        value2 = random.uniform(0, 255)
        for obs in self.obstacles:
            rect = obs["rect"]
            center = (rect.x + OBSTACLE_RADIUS, rect.y + OBSTACLE_RADIUS)

            # Draw halo if glowing using a transparent surface
            if now < obs["glow_until"]:
                glow_radius = OBSTACLE_RADIUS + 6
                glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (value, value1, value2, 200), (glow_radius, glow_radius), glow_radius)
                surface.blit(glow_surf, (center[0] - glow_radius, center[1] - glow_radius))

            # Base obstacle
            pygame.draw.circle(surface, OBSTACLE_COLOR, center, OBSTACLE_RADIUS)
        # Draw left and right walls
        # pygame.draw.rect(surface, (100, 100, 100), self.left_wall)   # Gray
        # pygame.draw.rect(surface, (100, 100, 100), self.right_wall)


    def check_collision(self, ball):
        """
        If the ball collides with any obstacle, invert its vertical velocity.
        Returns True if a collision occurred.
        """

        # Bounce off side walls
        if ball.get_rect().colliderect(self.left_wall):
            ball.vx = abs(ball.vx)
        elif ball.get_rect().colliderect(self.right_wall):
            ball.vx = -abs(ball.vx)

        value = random.uniform(-0.1, 0.1)
        ball_rect = ball.get_rect()
        for obs  in self.obstacles:
            rect = obs["rect"]
            if ball_rect.colliderect(rect):
                # invert vertical velocity
                ball.vy = -ball.vy / 1.1
                # push ball horizontally away from obstacle center
                obstacle_cx = rect.x + OBSTACLE_RADIUS

                if ball.x < obstacle_cx:# bounce left
                    ball.vx = -abs(ball.vx)
                else: # bounce right
                    ball.vx = abs(ball.vx)

                # Activate glow for GLOW_DURATION
                obs["glow_until"] = pygame.time.get_ticks() + GLOW_DURATION

                return True
        return False
