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
    HALO_COLORS,  # Import the list of halo colors
)

GLOW_DURATION = 300  # milliseconds - Increased for a more visible fade

NOTE_FOLDER = "notes"

pygame.init()
pygame.mixer.init()
# Load all note sounds into a list
note_sounds = []
for filename in os.listdir(NOTE_FOLDER):
    if filename.endswith(".wav") or filename.endswith(".ogg"):
        sound = pygame.mixer.Sound(os.path.join(NOTE_FOLDER, filename))
        sound.set_volume(0.7)
        note_sounds.append(sound)


class Obstacles:
    def __init__(self):

        wall_thickness = 10
        self.left_wall = pygame.Rect(100, 0, wall_thickness, SCREEN_HEIGHT)
        self.right_wall = pygame.Rect(SCREEN_WIDTH - (wall_thickness + 40), 0, wall_thickness, SCREEN_HEIGHT)
        # Build a grid of obstacle rects centered on (x, y)
        self.obstacles = []
        extra = 0
        for row in range(OBSTACLE_ROWS):
            for col in range(OBSTACLE_COLUMNS):
                extra = 0
                if (row % 2 == 0):
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
                    "glow_until": 0,  # timestamp in ms
                    "glow_color": None  # To store the color of the halo
                })

    def draw(self, surface):
        now = pygame.time.get_ticks()
        for obs in self.obstacles:
            rect = obs["rect"]
            center = (rect.x + OBSTACLE_RADIUS, rect.y + OBSTACLE_RADIUS)

            # Draw halo if glowing using a transparent surface
            if now < obs["glow_until"]:
                # Calculate the remaining glow time as a percentage
                remaining_glow = obs["glow_until"] - now
                alpha = 255 * (remaining_glow / GLOW_DURATION)
                alpha = max(0, min(255, alpha))  # Ensure alpha is within 0-255

                glow_radius = OBSTACLE_RADIUS + 12
                glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)

                # Use the stored glow_color and the calculated alpha
                color = (*obs["glow_color"], alpha)
                pygame.draw.circle(glow_surf, color, (glow_radius, glow_radius), glow_radius)
                surface.blit(glow_surf, (center[0] - glow_radius, center[1] - glow_radius))

            # Base obstacle
            pygame.draw.circle(surface, OBSTACLE_COLOR, center, OBSTACLE_RADIUS)

    def check_collision(self, ball):
        """
        Checks for and handles collisions between the ball and obstacles.
        """
        # Bounce off side walls
        if ball.get_rect().colliderect(self.left_wall):
            ball.vx = abs(ball.vx)
        elif ball.get_rect().colliderect(self.right_wall):
            ball.vx = -abs(ball.vx)

        for obs in self.obstacles:
            rect = obs["rect"]
            obstacle_center_x = rect.centerx
            obstacle_center_y = rect.centery

            # Vector from obstacle center to ball center
            dx = ball.x - obstacle_center_x
            dy = ball.y - obstacle_center_y
            distance = math.sqrt(dx * dx + dy * dy)

            # Check for collision
            if distance < OBSTACLE_RADIUS + ball.radius:
                # Collision detected!

                # To prevent sticking, move the ball slightly outside the obstacle
                overlap = (OBSTACLE_RADIUS + ball.radius) - distance
                ball.x += (dx / distance) * overlap
                ball.y += (dy / distance) * overlap

                # Calculate the reflection vector
                # Normal vector of the collision surface (from obstacle to ball)
                nx = dx / distance
                ny = dy / distance

                # Dot product of the velocity and the normal
                dot_product = ball.vx * nx + ball.vy * ny

                # Reflect the velocity vector
                ball.vx -= 2 * dot_product * nx
                ball.vy -= 2 * dot_product * ny

                # Activate glow for GLOW_DURATION and set a random color
                obs["glow_until"] = pygame.time.get_ticks() + GLOW_DURATION
                obs["glow_color"] = random.choice(HALO_COLORS)

                # Play a random musical note
                if note_sounds:
                    random.choice(note_sounds).play()

                return True
        return False

    def update_bucket_walls(self, wall_rects):
        # This function can be simplified or removed if the bucket walls are not part of the main obstacle list
        self.obstacles = [obs for obs in self.obstacles if obs.get("source") != "bucket_wall"]
        for rect in wall_rects:
            self.obstacles.append({
                "rect": rect,
                "glow_until": 0,
                "source": "bucket_wall"
            })