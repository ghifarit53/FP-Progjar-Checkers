import random
from constants import Colors, Constants

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
