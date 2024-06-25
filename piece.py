# piece.py
import pygame
from constants import Constants, Colors

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0

    def calculate_position(self, square_size):
        self.x = self.col * square_size + square_size // 2
        self.y = self.row * square_size + square_size // 2

    def make_king(self):
        self.king = True

    def draw(self, surface, square_size):
        self.calculate_position(square_size)
        radius = max(square_size // 2 - self.PADDING, 8)
        pygame.draw.circle(surface, Colors.GREEN, (self.x, self.y), radius + self.OUTLINE)  # Draw the outline
        pygame.draw.circle(surface, self.color, (self.x, self.y), radius)
        if self.king:
            pygame.draw.circle(surface, Colors.WHITE, (self.x, self.y), radius // 2)

    def get_valid_moves(self, board):
        valid_moves = []
        directions = [-1, 1]
        row = self.row
        col = self.col
        forward = 1 if self.color == Colors.BLACK else -1

        for direction in directions:
            if self.can_jump(row + forward, col + direction, row + 2 * forward, col + 2 * direction, board):
                valid_moves.append((row + 2 * forward, col + 2 * direction))
            elif self.is_valid_move(row + forward, col + direction, board):
                valid_moves.append((row + forward, col + direction))

        if self.king:
            for direction in directions:
                if self.can_jump(row - forward, col + direction, row - 2 * forward, col + 2 * direction, board):
                    valid_moves.append((row - 2 * forward, col + 2 * direction))
                elif self.is_valid_move(row - forward, col + direction, board):
                    valid_moves.append((row - forward, col + direction))

        return valid_moves

    def is_valid_move(self, row, col, board):
        if row < 0 or row >= Constants.ROWS or col < 0 or col >= Constants.COLS:
            return False
        if board[row][col] != 0:
            return False
        return True

    def can_jump(self, start_row, start_col, end_row, end_col, board):
        if end_row < 0 or end_row >= Constants.ROWS or end_col < 0 or end_col >= Constants.COLS:
            return False
        if board[end_row][end_col] != 0:
            return False
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
