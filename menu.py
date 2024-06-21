import pygame
from constants import Constants, Colors

def draw_menu(surface, font):
    surface.fill(Colors.MENU_BG)
    
    # Example menu options (customize as needed)
    text = font.render("Checkers 101", True, Colors.TEXT_COLOR)
    text_rect = text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 4))
    surface.blit(text, text_rect)

    pvp_button = pygame.Rect(Constants.WIDTH // 4, Constants.HEIGHT // 2, Constants.WIDTH // 2, 50)
    pvp_text = font.render("Player vs Player", True, Colors.TEXT_COLOR)
    pvp_text_rect = pvp_text.get_rect(center=pvp_button.center)
    pygame.draw.rect(surface, Colors.BUTTON_COLOR, pvp_button)
    surface.blit(pvp_text, pvp_text_rect)

    pvai_button = pygame.Rect(Constants.WIDTH // 4, Constants.HEIGHT // 2 + 100, Constants.WIDTH // 2, 50)
    pvai_text = font.render("Player vs AI", True, Colors.TEXT_COLOR)
    pvai_text_rect = pvai_text.get_rect(center=pvai_button.center)
    pygame.draw.rect(surface, Colors.BUTTON_COLOR, pvai_button)
    surface.blit(pvai_text, pvai_text_rect)

    pygame.display.flip()
