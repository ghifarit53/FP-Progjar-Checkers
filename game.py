import pygame
from ai import get_ai_move

def handle_player_turn(board, surface, player_turn):
    if player_turn:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if board.handle_click(pos):
                    return False  # ENd of Player turn
    return True

def handle_ai_turn(board, surface, ai_turn):
    if ai_turn:
        ai_move = get_ai_move(board)
        if ai_move:
            piece, (row, col) = ai_move
            board.move(piece, row, col)
            return False  # End of AI turn
    return True
