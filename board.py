import pygame
from constants import Constants, Colors
from piece import Piece

class Board:
    def __init__(self):
        self.board = []  # 2D list to store pieces
        self.setup_board()

    def setup_board(self):
        # Set up the initial board configuration with pieces
        for row in range(Constants.ROWS):
            self.board.append([])
            for col in range(Constants.COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, Colors.LIGHT_BROWN))  # Add light brown pieces
                    elif row > 4:
                        self.board[row].append(Piece(row, col, Colors.BLACK))  # Add black pieces
                    else:
                        self.board[row].append(0)  # Empty square
                else:
                    self.board[row].append(0)  # Empty square

    def draw(self, surface):
        # Get the width and height of the surface
        width, height = surface.get_size()
        # Calculate square size based on surface dimensions
        square_size = min(width // Constants.COLS, height // Constants.ROWS)

        # Fill the surface with the background color
        surface.fill(Colors.BLACK)

        # Draw the squares on the board
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                rect = (col * square_size, row * square_size, square_size, square_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(surface, Colors.LIGHT_SQUARE, rect)
                else:
                    pygame.draw.rect(surface, Colors.DARK_SQUARE, rect)

        # Draw the board and pieces
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(surface, square_size)