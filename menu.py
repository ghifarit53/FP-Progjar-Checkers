import pygame
from constants import Constants, Colors

def draw_menu(surface, font):
    surface.fill(Colors.BLACK)  # Matrix theme
    
    # Menu options (customize as needed, please)
    title_text = font.render("Checkers 101", True, Colors.GREEN)
    title_rect = title_text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 4))
    surface.blit(title_text, title_rect)

    # Player vs Player button
    pvp_button = pygame.Rect(Constants.WIDTH // 4, Constants.HEIGHT // 2, Constants.WIDTH // 2, 50)
    pygame.draw.rect(surface, Colors.GREEN, pvp_button, 2)
    pygame.draw.rect(surface, Colors.BUTTON_COLOR, pvp_button)
    pvp_text = font.render("Player vs Player", True, Colors.GREEN)
    pvp_text_rect = pvp_text.get_rect(center=pvp_button.center)
    surface.blit(pvp_text, pvp_text_rect)

    # Player vs AI button
    pvai_button = pygame.Rect(Constants.WIDTH // 4, Constants.HEIGHT // 2 + 100, Constants.WIDTH // 2, 50)
    pygame.draw.rect(surface, Colors.GREEN, pvai_button, 2)  # Green border
    pygame.draw.rect(surface, Colors.BUTTON_COLOR, pvai_button)
    pvai_text = font.render("Player vs AI", True, Colors.GREEN)
    pvai_text_rect = pvai_text.get_rect(center=pvai_button.center)
    surface.blit(pvai_text, pvai_text_rect)

    pygame.display.flip()