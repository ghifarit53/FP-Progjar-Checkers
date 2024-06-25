# main.py
import pygame
import os
from constants import Constants, Colors
from board import Board
from menu import draw_menu

def main():
    pygame.init()
    aspect_ratio = Constants.WIDTH / Constants.HEIGHT
    min_width, min_height = 300, 300
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Checkers 101')

    # Load font
    font_path = os.path.join('assets', 'fonts', 'audiowide-mono', 'Audiowide-Mono-301.ttf')
    font = pygame.font.Font(font_path, 23)

    board = Board()
    clock = pygame.time.Clock()
    running = True
    menu_active = True
    game_mode = None
    turn = "player1"

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
                    if pvp_button.collidepoint(pos):
                        menu_active = False
                        game_mode = "pvp"
                        turn = "player1"

            if not menu_active and game_mode == "pvp":
                surface.fill(Colors.BLACK)
                board.draw(surface)
                pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        if board.handle_click(pos):
                            turn = "player2" if turn == "player1" else "player1"

    pygame.quit()

if __name__ == '__main__':
    main()
