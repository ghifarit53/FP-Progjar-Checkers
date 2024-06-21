import pygame
from constants import Constants, Colors

class Piece:
    PADDING = 15  # Padding around the piece to make it smaller than the square
    OUTLINE = 2  # Outline thickness of the piece

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False  # Initially, the piece is not a king
        self.x = 0
        self.y = 0

    def calculate_position(self, square_size):
        self.x = self.col * square_size + square_size // 2
        self.y = self.row * square_size + square_size // 2

    def make_king(self):
        # Promote the piece to a king
        self.king = True

    def draw(self, surface, square_size):
        self.calculate_position(square_size)
        radius = max(square_size // 2 - self.PADDING, 8)
        pygame.draw.circle(surface, Colors.HIGHLIGHT, (self.x, self.y), radius + self.OUTLINE)  # Draw the outline
        pygame.draw.circle(surface, self.color, (self.x, self.y), radius)  # Draw the piece
        if self.king:
            pygame.draw.circle(surface, Colors.WHITE, (self.x, self.y), radius // 2)  # Draw a smaller circle for kings

    def get_valid_moves(self, board):
        valid_moves = []

        # Implement logic here to determine valid moves for the piece
        # Example logic:
        # Check diagonal moves (left and right)
        # Example for single move (without capturing) to the right
        if self.row + 1 < Constants.ROWS and self.col + 1 < Constants.COLS:
            if board[self.row + 1][self.col + 1] == 0:  # Check if the square is empty
                valid_moves.append((self.row + 1, self.col + 1))

        # You should implement more comprehensive logic here for capturing moves and kings

        return valid_moves

    def __repr__(self):
        return str(self.color)  # Return the color of the piece as its string representation
