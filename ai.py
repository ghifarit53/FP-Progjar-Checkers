import random
from constants import Colors, Constants

def get_ai_move(board, turn):
    moves = []
    
    # Determine which color the AI should control based on the turn
    ai_color = Colors.BLACK if turn == "ai" else Colors.RED

    # Collect all possible moves for pieces of the AI's color
    for row in range(Constants.ROWS):
        for col in range(Constants.COLS):
            piece = board.board[row][col]
            if piece != 0 and piece.color == ai_color:
                valid_moves = board.get_valid_moves(piece)
                for move in valid_moves:
                    moves.append((piece, move))

    # If no moves are available, return None
    if not moves:
        return None
    
    # Choose a random move from the list of valid moves
    return random.choice(moves)
