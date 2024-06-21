import pygame
import os  # To handle file paths
import random
from constants import Constants, Colors
from board import Board
from menu import draw_menu

# AI function to get a random move
def get_ai_move(board):
    moves = []
    # Count possible moves based on rows
    for row in range(Constants.ROWS):
        for col in range(Constants.COLS):
            piece = board.board[row][col]
            if piece != 0 and piece.color == Colors.BLACK:
                valid_moves = board.get_valid_moves(piece)
                for move in valid_moves:
                    moves.append((piece, move))
    if not moves:
        return None
    return random.choice(moves)

def main():
    pygame.init()
    aspect_ratio = Constants.WIDTH / Constants.HEIGHT
    min_width, min_height = 600, 600
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Checkers')

    # Load monospace font
    font_path = os.path.join('assets', 'fonts', 'audiowide-mono', 'Audiowide-Mono-Latest.ttf')
    font = pygame.font.Font(font_path, 23)  # Adjust size as needed

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
                        turn = "player1"  # Set turn to player 1
                    elif pvai_button.collidepoint(pos):
                        menu_active = False
                        game_mode = "pvai"
                        turn = "player1"  # Set turn to player 1

        if not menu_active:
            surface.fill(Colors.BLACK)
            board.draw(surface)
            pygame.display.flip()

            if game_mode == "pvp":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        if board.handle_click(pos):
                            turn = "player2" if turn == "player1" else "player1"  # Switch turns in player vs player mode

            elif game_mode == "pvai":
                if turn == "player1":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            pos = pygame.mouse.get_pos()
                            if board.handle_click(pos):
                                turn = "ai"  # Switch to AI's turn

                elif turn == "ai":
                    # Simulate AI move
                    ai_move = get_ai_move(board)
                    if ai_move:
                        piece, move = ai_move
                        board.move_piece(piece, move)
                    turn = "player1"  # Switch back to player 1's turn after AI move

    pygame.quit()

if __name__ == '__main__':
    main()
