# info_panel.py

import pygame
from settings import (
    SCREEN_HEIGHT,
    INFO_PANEL_WIDTH,
    INFO_PANEL_COLOR,
    INFO_TEXT_COLOR,
    INFO_FONT_SIZE,
    INFO_PANEL_BORDER_COLOR,
    INFO_PANEL_TITLE_COLOR
)

class InfoPanel:
    def __init__(self):
        self.width = INFO_PANEL_WIDTH
        self.x = 0
        self.y = 0
        self.height = SCREEN_HEIGHT
        try:
            self.title_font = pygame.font.SysFont("Orbitron", INFO_FONT_SIZE + 4)
        except:
            self.title_font = pygame.font.SysFont(None, INFO_FONT_SIZE + 4)
        self.font = pygame.font.SysFont(None, INFO_FONT_SIZE)
        self.info_lines = ["Welcome!", "Score x100", "Balls active: 0"]

    def update_info(self, lines):
        """Update the list of lines to display"""
        self.info_lines = lines

    def draw(self, surface):
        # Draw panel background
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, INFO_PANEL_COLOR, panel_rect)

        # Draw a border to make it pop
        pygame.draw.rect(surface, INFO_PANEL_BORDER_COLOR, panel_rect, 3)

        # Draw the title
        title_text = "INFO"
        title_surf = self.title_font.render(title_text, True, INFO_PANEL_TITLE_COLOR)
        title_rect = title_surf.get_rect(center=(self.width / 2, 30))
        surface.blit(title_surf, title_rect)

        # Draw a separator line
        pygame.draw.line(surface, INFO_PANEL_BORDER_COLOR, (self.x + 10, 50), (self.width - 10, 50), 2)

        # Draw each line of info
        for i, line in enumerate(self.info_lines):
            # If this is the cost line, draw a white box behind the value
            if line.startswith("COST:"):
                # Position for the white box (behind the number)
                box_x = self.x + 50
                box_y = 70 + i * 30
                pygame.draw.rect(surface, (255, 255, 255), (box_x, box_y, 40, 20))
                # Render the text with a black color to be visible on the white box
                text_surf = self.font.render(line, True, INFO_TEXT_COLOR)
                surface.blit(text_surf, (self.x + 10, 70 + i * 30))
                # Draw the number part in black
                cost_value_text = line.split(" ")[1]
                cost_surf = self.font.render(cost_value_text, True, (0,0,0)) # Black color
                surface.blit(cost_surf, (box_x + 5, box_y + 2))

            else:
                text_surf = self.font.render(line, True, INFO_TEXT_COLOR)
                surface.blit(text_surf, (self.x + 10, 70 + i * 30))