# menu.py
import pygame
from constants import Constants, Colors

def draw_menu(surface, font):
    surface.fill(Colors.MENU_BG)
    text_color = Colors.TEXT_COLOR
    button_color = Colors.BUTTON_COLOR

    title_text = font.render('Checkers', True, text_color)
    pvp_text = font.render('Player vs Player', True, text_color)

    title_rect = title_text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 4))
    pvp_rect = pvp_text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2))

    pygame.draw.rect(surface, button_color, pvp_rect.inflate(20, 20))
    surface.blit(title_text, title_rect)
    surface.blit(pvp_text, pvp_rect)

    pygame.display.update()
