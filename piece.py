import pygame
from constants import Constants, Colors

class Piece:
    PADDING = 15  # Padding around the piece
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
        # Draw bright green border around the piece
        pygame.draw.circle(surface, Colors.GREEN, (self.x, self.y), radius + self.OUTLINE)  # Draw the outline
        pygame.draw.circle(surface, self.color, (self.x, self.y), radius)  # Draw the piece
        if self.king:
            pygame.draw.circle(surface, Colors.WHITE, (self.x, self.y), radius // 2)  # Draw a smaller circle for kings

    def get_valid_moves(self, board):
        valid_moves = []
        directions = [-1, 1]
        row = self.row
        col = self.col

        # Check forward moves based on piece color (assuming upwards is +ve row direction)
        forward = 1 if self.color == Colors.BLACK else -1

        # Check diagonal moves (left and right)
        for direction in directions:
            if self.can_jump(row + forward, col + direction, row + 2 * forward, col + 2 * direction, board):
                valid_moves.append((row + 2 * forward, col + 2 * direction))

        # If the piece = king, check backward moves
        if self.king:
            for direction in directions:
                if self.can_jump(row - forward, col + direction, row - 2 * forward, col + 2 * direction, board):
                    valid_moves.append((row - 2 * forward, col + 2 * direction))

        return valid_moves

    def can_jump(self, start_row, start_col, end_row, end_col, board):
        # Check if the move is within bounds of the board
        if end_row < 0 or end_row >= Constants.ROWS or end_col < 0 or end_col >= Constants.COLS:
            return False

        # Check if the target position is empty
        if board[end_row][end_col] != 0:
            return False

        # Check if there is an opponent's piece to jump over
        opponent_row = (start_row + end_row) // 2
        opponent_col = (start_col + end_col) // 2
        if board[opponent_row][opponent_col] == 0 or board[opponent_row][opponent_col].color == self.color:
            return False

        return True

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col

    def __repr__(self):
        return str(self.color)
