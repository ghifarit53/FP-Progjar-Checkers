import pygame
from constants import Constants, Colors

def draw_menu(surface, font):
    surface.fill(Colors.MENU_BG)
    text_color = Colors.TEXT_COLOR
    button_color = Colors.BUTTON_COLOR
    border_color = Colors.GREEN  # Adjust this color as needed

    title_text = font.render('Checkers 101', True, text_color)
    pvp_text = font.render(' P v P ', True, text_color)

    title_rect = title_text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 4))
    pvp_rect = pvp_text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2))

    # Set button width to match title width, with padding
    button_width = title_rect.width + 40  # Horizontal padding adjustment
    button_height = pvp_rect.height + 20  # Vertical padding adjustment increased by 10 units
    button_rect = pygame.Rect((Constants.WIDTH - button_width) // 2, Constants.HEIGHT // 2, button_width, button_height)

    # Draw bright green border
    pygame.draw.rect(surface, border_color, button_rect)
    pygame.draw.rect(surface, button_color, button_rect.inflate(-4, -4))  # Inner rectangle for button color

    # Center text within the button
    text_x = button_rect.centerx - pvp_rect.width // 2
    text_y = button_rect.centery - pvp_rect.height // 2
    surface.blit(pvp_text, (text_x, text_y))

    surface.blit(title_text, title_rect)

    pygame.display.update()
