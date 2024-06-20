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

    def draw_squares(self, surface):
        # Draw the squares on the board
        surface.fill(Colors.BLACK)
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(surface, Colors.LIGHT_SQUARE, 
                                     (col * Constants.SQUARE_SIZE, row * Constants.SQUARE_SIZE, 
                                      Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))
                else:
                    pygame.draw.rect(surface, Colors.DARK_SQUARE, 
                                     (col * Constants.SQUARE_SIZE, row * Constants.SQUARE_SIZE, 
                                      Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))

    def draw(self, surface):
        # Draw the board and pieces
        self.draw_squares(surface)
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(surface)
