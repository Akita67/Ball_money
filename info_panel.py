# info_panel.py

import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    INFO_PANEL_WIDTH, INFO_PANEL_COLOR,
    INFO_TEXT_COLOR, INFO_FONT_SIZE
)

class InfoPanel:
    def __init__(self):
        self.width = INFO_PANEL_WIDTH
        self.x = SCREEN_WIDTH - self.width
        self.y = 0
        self.height = SCREEN_HEIGHT
        self.font = pygame.font.SysFont(None, INFO_FONT_SIZE)
        self.info_lines = ["Welcome!", "Score x100", "Balls active: 0"]

    def update_info(self, lines):
        """Update the list of lines to display"""
        self.info_lines = lines

    def draw(self, surface):
        # Draw panel background
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, INFO_PANEL_COLOR, panel_rect)

        # Draw each line of info
        for i, line in enumerate(self.info_lines):
            text_surf = self.font.render(line, True, INFO_TEXT_COLOR)
            surface.blit(text_surf, (self.x + 10, 20 + i * 30))
