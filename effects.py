import pygame
import random

# --- HELPER CLASS FOR SCORE EFFECT ---
class Particle:
    """Represents a single particle for the scoring explosion effect."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Give it a random upward and outward velocity
        self.vx = random.uniform(-2.5, 2.5)
        self.vy = random.uniform(-4, -1)
        self.lifespan = random.randint(30, 60) # How long it lives, in frames
        self.color = (random.randint(200, 255), random.randint(180, 255), random.randint(0, 50)) # Gold/Yellow/Orange
        self.radius = random.randint(2, 5)

    def update(self):
        """Move the particle and decrease its lifespan."""
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1

    def draw(self, surface):
        """Draw the particle, making it fade out as it dies."""
        # Calculate alpha based on remaining lifespan to create a fade-out effect
        alpha = max(0, 255 * (self.lifespan / 60))
        # Create a temporary surface to handle transparency
        temp_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surf, (*self.color, alpha), (self.radius, self.radius), self.radius)
        surface.blit(temp_surf, (self.x - self.radius, self.y - self.radius))

# --- HELPER CLASS FOR FLOATING SCORE TEXT ---
class FloatingText:
    """Represents a floating text object, like '+250' when scoring."""
    def __init__(self, x, y, text, font):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.lifespan = 75  # Lives for 75 frames
        self.vy = -1  # Moves upwards

    def update(self):
        """Move the text up and decrease its lifespan."""
        self.y += self.vy
        self.lifespan -= 1

    def draw(self, surface):
        """Draw the text, making it fade out over time."""
        alpha = max(0, 255 * (self.lifespan / 75))
        text_surf = self.font.render(self.text, True, (255, 255, 150)) # Bright yellow
        text_surf.set_alpha(alpha)
        surface.blit(text_surf, (self.x, self.y))
