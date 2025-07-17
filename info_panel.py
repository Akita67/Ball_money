# info_panel.py

import pygame
from settings import (
    SCREEN_HEIGHT,
    INFO_PANEL_WIDTH,
    UI_PANEL_COLOR,
    UI_TEXT_COLOR,
    UI_TEXT_BRIGHT_COLOR,
    UI_INPUT_BOX_COLOR,
    UI_ACCENT_COLOR,  # Import the green accent color
    INFO_FONT_NAME,
    INFO_FONT_SIZE,
    MULTIPLIER, BALL_COST
)

class InfoPanel:
    def __init__(self):
        self.width = INFO_PANEL_WIDTH
        self.height = SCREEN_HEIGHT
        self.x = 0
        self.y = 0
        self.font_sm = pygame.font.SysFont(INFO_FONT_NAME, INFO_FONT_SIZE - 2)
        self.font_md = pygame.font.SysFont(INFO_FONT_NAME, INFO_FONT_SIZE)
        self.font_lg = pygame.font.SysFont(INFO_FONT_NAME, INFO_FONT_SIZE + 2, bold=True)


        # Helper to create the layout
        self.ui_elements = {}
        self.add_ui_element("score", "BALANCE", 50)
        self.add_ui_element("balls", "BALLS", 120)
        self.add_ui_element("time", "TIME", 190)
        self.add_ui_element("cost", "COST", 260)
        self.add_ui_element("multiplier", "MULTIPLIER", 330)

        # Add the start button
        self.start_button_rect = pygame.Rect(self.x + 15, 420, self.width - 30, 50)


    def add_ui_element(self, key, label, y_pos):
        self.ui_elements[key] = {
            "label": label,
            "rect": pygame.Rect(self.x + 15, y_pos, self.width - 30, 40)
        }

    def _draw_element(self, surface, element, value_text):
        # Draw label
        label_surf = self.font_sm.render(element["label"], True, UI_TEXT_COLOR)
        surface.blit(label_surf, (element["rect"].x, element["rect"].y - 20))

        # Draw box
        pygame.draw.rect(surface, UI_INPUT_BOX_COLOR, element["rect"], border_radius=5)

        # Draw value
        value_surf = self.font_md.render(str(value_text), True, UI_TEXT_BRIGHT_COLOR)
        surface.blit(value_surf, (element["rect"].x + 10, element["rect"].y + 12))


    def draw(self, surface, score, balls, time, cost, multiplier):
        # Main background
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, UI_PANEL_COLOR, panel_rect)

        # Draw all the data elements
        self._draw_element(surface, self.ui_elements["score"], f"{score:.1f}")
        self._draw_element(surface, self.ui_elements["balls"], balls)
        self._draw_element(surface, self.ui_elements["time"], f"{time}s")
        self._draw_element(surface, self.ui_elements["cost"], f"{cost:.1f}$")
        self._draw_element(surface, self.ui_elements["multiplier"], f"X{MULTIPLIER*BALL_COST}")

        # --- Draw Start Button ---
        pygame.draw.rect(surface, UI_ACCENT_COLOR, self.start_button_rect, border_radius=5)
        start_text_surf = self.font_lg.render("Start Autobet", True, (0, 0, 0)) # Black text
        start_text_rect = start_text_surf.get_rect(center=self.start_button_rect.center)
        surface.blit(start_text_surf, start_text_rect)

    def is_start_button_clicked(self, pos):
        """Check if the given position is within the start button's bounds."""
        return self.start_button_rect.collidepoint(pos)