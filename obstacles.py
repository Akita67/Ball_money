# obstacles.py

import pygame
import random
import os
import math

from settings import (
    OBSTACLE_COLOR, OBSTACLE_RADIUS,
    OBSTACLE_COLUMNS, OBSTACLE_ROWS,
    OBSTACLE_OFFSET_X, OBSTACLE_OFFSET_Y,
    OBSTACLE_SPACING_X, OBSTACLE_SPACING_Y,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    HALO_COLORS,
)

GLOW_DURATION = 300  # milliseconds

NOTE_FOLDER = "notes"

pygame.init()
pygame.mixer.init()

note_sounds = []
if os.path.exists(NOTE_FOLDER):
    for filename in os.listdir(NOTE_FOLDER):
        if filename.endswith(".wav") or filename.endswith(".ogg"):
            sound = pygame.mixer.Sound(os.path.join(NOTE_FOLDER, filename))
            sound.set_volume(0.7)
            note_sounds.append(sound)


class Obstacles:
    def __init__(self):
        self.wall_thickness = 10
        self.left_wall = pygame.Rect(100, 0, self.wall_thickness, SCREEN_HEIGHT)
        self.right_wall = pygame.Rect(SCREEN_WIDTH - (self.wall_thickness ), 0, self.wall_thickness, SCREEN_HEIGHT)

        self.peg_obstacles = []
        extra = 0
        for row in range(OBSTACLE_ROWS):
            for col in range(OBSTACLE_COLUMNS):
                extra = 0
                if row % 2 == 0:
                    extra = 50
                x = OBSTACLE_OFFSET_X + col * OBSTACLE_SPACING_X + extra
                y = OBSTACLE_OFFSET_Y + row * OBSTACLE_SPACING_Y
                self.peg_obstacles.append({
                    "center_x": x,
                    "center_y": y,
                    "glow_until": 0,
                    "glow_color": None
                })
        self.bucket_walls = []

    def draw(self, surface):
        now = pygame.time.get_ticks()
        for obs in self.peg_obstacles:
            center = (obs["center_x"], obs["center_y"])
            if now < obs["glow_until"]:
                remaining_glow = obs["glow_until"] - now
                alpha = 255 * (remaining_glow / GLOW_DURATION)
                alpha = max(0, min(255, alpha))
                glow_radius = OBSTACLE_RADIUS + 12
                glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                color = (*obs["glow_color"], alpha)
                pygame.draw.circle(glow_surf, color, (glow_radius, glow_radius), glow_radius)
                surface.blit(glow_surf, (center[0] - glow_radius, center[1] - glow_radius))
            pygame.draw.circle(surface, OBSTACLE_COLOR, center, OBSTACLE_RADIUS)

    def check_collision(self, ball):
        # This function now checks for all collisions but doesn't stop the game logic flow.

        # --- Bounce off side walls ---
        if ball.get_rect().colliderect(self.left_wall) or ball.get_rect().colliderect(self.right_wall):
            ball.vx *= -1

        # --- Bounce off Pegs (Circular Collision) ---
        for obs in self.peg_obstacles:
            dx = ball.x - obs["center_x"]
            dy = ball.y - obs["center_y"]
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < OBSTACLE_RADIUS + ball.radius:
                overlap = (OBSTACLE_RADIUS + ball.radius) - distance
                ball.x += (dx / distance) * overlap
                ball.y += (dy / distance) * overlap
                nx = dx / distance
                ny = dy / distance
                dot_product = ball.vx * nx + ball.vy * ny
                ball.vx -= 2 * dot_product * nx
                ball.vy -= 2 * dot_product * ny
                obs["glow_until"] = pygame.time.get_ticks() + GLOW_DURATION
                obs["glow_color"] = random.choice(HALO_COLORS)
                if note_sounds:
                    random.choice(note_sounds).play()

        # --- Bounce off Bucket Walls (Rectangular Collision) ---
        for wall_rect in self.bucket_walls:
            if ball.get_rect().colliderect(wall_rect):
                ball.vx *= -1.1
                if ball.x < wall_rect.centerx:
                    ball.x = wall_rect.left - ball.radius
                else:
                    ball.x = wall_rect.right + ball.radius

    def update_bucket_walls(self, wall_rects):
        self.bucket_walls = wall_rects