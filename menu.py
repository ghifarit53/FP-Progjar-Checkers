import pygame
from constants import Colors, Constants

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)
        self.buttons = [
            {"text": "Start Game", "rect": pygame.Rect(200, 200, 200, 50), "color": Colors.LIGHT_SQUARE},
            {"text": "Quit", "rect": pygame.Rect(200, 300, 200, 50), "color": Colors.LIGHT_SQUARE}
        ]
        self.hover_index = None

    def draw(self, surface):
        surface.fill(Colors.DARK_SQUARE)  
        for i, button in enumerate(self.buttons):
            color = Colors.HIGHLIGHT if i == self.hover_index else button["color"]
            pygame.draw.rect(surface, color, button["rect"], border_radius=12)
            text_surface = self.font.render(button["text"], True, Colors.BLACK)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            surface.blit(text_surface, text_rect)

    def get_button(self, position):
        for i, button in enumerate(self.buttons):
            if button["rect"].collidepoint(position):
                self.hover_index = i
                return button["text"]
        self.hover_index = None
        return None

    def update_hover(self, position):
        self.get_button(position)
