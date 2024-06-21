import pygame
from constants import Constants, Colors
from board import Board
from menu import draw_menu

def main():
    pygame.init()
    aspect_ratio = Constants.WIDTH / Constants.HEIGHT
    min_width, min_height = 300, 300
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Checkers')

    font = pygame.font.Font(None, 36)
    board = Board()
    clock = pygame.time.Clock()
    running = True
    menu_active = True
    game_mode = None

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                new_width = max(event.w, min_width)
                new_height = max(event.h, min_height)
                if new_width / new_height > aspect_ratio:
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_height = int(new_width / aspect_ratio)
                surface = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            if menu_active:
                draw_menu(surface, font)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pvp_button = pygame.Rect(Constants.WIDTH // 4, Constants.HEIGHT // 2, Constants.WIDTH // 2, 50)
                    pvai_button = pygame.Rect(Constants.WIDTH // 4, Constants.HEIGHT // 2 + 100, Constants.WIDTH // 2, 50)
                    if pvp_button.collidepoint(pos):
                        menu_active = False
                        game_mode = "pvp"
                    elif pvai_button.collidepoint(pos):
                        menu_active = False
                        game_mode = "pvai"

        if not menu_active:
            surface.fill(Colors.BLACK)
            board.draw(surface)
            pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    board.handle_click(pos)

    pygame.quit()

if __name__ == '__main__':
    main()
