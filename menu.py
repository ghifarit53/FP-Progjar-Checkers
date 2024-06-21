import pygame
from constants import Constants, Colors

def draw_menu(surface, font):
    surface.fill(Colors.MENU_BG)
    title = font.render("Checkers", True, Colors.TEXT_COLOR)
    title_rect = title.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 4))
    surface.blit(title, title_rect)

    player_vs_player = font.render("Player vs Player", True, Colors.BUTTON_COLOR)
    player_vs_ai = font.render("Player vs AI", True, Colors.BUTTON_COLOR)

    pvp_rect = player_vs_player.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2))
    pvai_rect = player_vs_ai.get_rect(center=(Constants.WIDTH // 2, 3 * Constants.HEIGHT // 4))

    surface.blit(player_vs_player, pvp_rect)
    surface.blit(player_vs_ai, pvai_rect)

    return pvp_rect, pvai_rect
