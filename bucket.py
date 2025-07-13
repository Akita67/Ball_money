import pygame
from settings import BUCKET_WIDTH, BUCKET_HEIGHT, BUCKET_COLOR, BUCKET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Bucket:
    def __init__(self):
        self.x = (SCREEN_WIDTH - BUCKET_WIDTH) / 2
        self.y = SCREEN_HEIGHT - BUCKET_HEIGHT - 10  # 10 px margin
        self.direction = 1  # 1 = moving right; -1 = moving left

    def update(self):
        # Move bucket
        self.x += BUCKET_SPEED * self.direction

        # Bounce off edges
        if self.x <= 0:
            self.x = 0
            self.direction = 1
        elif self.x >= SCREEN_WIDTH - BUCKET_WIDTH:
            self.x = SCREEN_WIDTH - BUCKET_WIDTH
            self.direction = -1

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, BUCKET_WIDTH, BUCKET_HEIGHT)
        pygame.draw.rect(surface, BUCKET_COLOR, rect)
        wall_l = pygame.Rect(self.x, self.y - 20, BUCKET_HEIGHT, BUCKET_WIDTH/2)
        pygame.draw.rect(surface, BUCKET_COLOR, wall_l)
        wall_r = pygame.Rect(self.x + 40, self.y - 20, BUCKET_HEIGHT, BUCKET_WIDTH / 2)
        pygame.draw.rect(surface, BUCKET_COLOR, wall_r)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, BUCKET_WIDTH, BUCKET_HEIGHT)
