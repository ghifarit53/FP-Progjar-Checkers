import pygame
from constants import Constants, Colors

def play_vs_player(board, pos):
    if board.handle_click(pos):
        return True
    return False

def play_vs_ai(board):
    import random
    valid_pieces = []
    for row in range(Constants.ROWS):
        for col in range(Constants.COLS):
            piece = board.board[row][col]
            if piece != 0 and piece.color == Colors.BLACK:  # Use Colors.BLACK instead of Constants.BLACK
                valid_pieces.append((row, col))
    if valid_pieces:
        piece_to_move = random.choice(valid_pieces)
        board.handle_click((piece_to_move[1] * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2,
                            piece_to_move[0] * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2))
        # Simulate a random valid move for demonstration purposes
        valid_moves = board.board[piece_to_move[0]][piece_to_move[1]].get_valid_moves(board.board)
        if valid_moves:
            move = random.choice(valid_moves)
            board.handle_click((move[1] * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2,
                                move[0] * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2))
