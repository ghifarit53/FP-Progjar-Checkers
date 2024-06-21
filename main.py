import pygame
from constants import Constants, Colors
from board import Board
from menu import draw_menu
from game import play_vs_player, play_vs_ai

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
    turn = "player1"  # Initialize turn tracker

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
                        turn = "player1"  # Start with player 1's turn against AI

        if not menu_active:
            surface.fill(Colors.BLACK)
            board.draw(surface)
            pygame.display.flip()

            if game_mode == "pvp":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        if turn == "player1":
                            if play_vs_player(board, pos):
                                turn = "player2"  # Switch to player 2's turn
                        else:
                            if play_vs_player(board, pos):
                                turn = "player1"  # Switch to player 1's turn

            elif game_mode == "pvai":
                if turn == "player1":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            pos = pygame.mouse.get_pos()
                            if play_vs_player(board, pos):
                                turn = "ai"  # Switch to AI's turn

                elif turn == "ai":
                    # AI logic goes here
                    play_vs_ai(board)
                    turn = "player1"  # Switch back to player 1's turn after AI move

    pygame.quit()

if __name__ == '__main__':
    main()