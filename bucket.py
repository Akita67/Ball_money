import pygame
from settings import BUCKET_WIDTH, BUCKET_HEIGHT, BUCKET_COLOR, BUCKET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, MULTIPLIER, BALL_COST

class Bucket:
    def __init__(self):
        self.x = (SCREEN_WIDTH - BUCKET_WIDTH) / 2
        self.y = SCREEN_HEIGHT - BUCKET_HEIGHT - 10  # 10 px margin
        self.direction = 1  # 1 = moving right; -1 = moving left
        self.wall_height = BUCKET_WIDTH / 2
        self.wall_thickness = 4 # A bit thicker for better collision

    def update(self):
        # Move bucket
        self.x += BUCKET_SPEED * self.direction

        # Bounce off edges
        if self.x <= 100:
            self.x = 100
            self.direction = 1
        elif self.x >= SCREEN_WIDTH - BUCKET_WIDTH:
            self.x = SCREEN_WIDTH - BUCKET_WIDTH
            self.direction = -1

    def draw(self, surface):
        # Draw the base of the bucket
        base_rect = pygame.Rect(self.x, self.y, BUCKET_WIDTH, BUCKET_HEIGHT)
        pygame.draw.rect(surface, BUCKET_COLOR, base_rect)

        # Draw the walls
        for wall in self.get_wall_rects():
            pygame.draw.rect(surface, BUCKET_COLOR, wall)

        # Draw the text "X100" above the bucket
        font = pygame.font.SysFont("Orbitron", 24)
        text_surface = font.render(f"X{MULTIPLIER*BALL_COST}", True, (255, 255, 255))  # white color
        text_rect = text_surface.get_rect(center=(self.x + BUCKET_WIDTH / 2, self.y - 30))
        surface.blit(text_surface, text_rect)


    def get_rect(self):
        # This is the area that collects the ball for scoring
        return pygame.Rect(self.x + self.wall_thickness, self.y, BUCKET_WIDTH - (self.wall_thickness * 2), BUCKET_HEIGHT)

    def get_wall_rects(self):
        # Define the two vertical walls of the bucket
        left_wall = pygame.Rect(self.x, self.y - self.wall_height, self.wall_thickness, self.wall_height)
        right_wall = pygame.Rect(self.x + BUCKET_WIDTH - self.wall_thickness, self.y - self.wall_height, self.wall_thickness, self.wall_height)
        return [left_wall, right_wall]