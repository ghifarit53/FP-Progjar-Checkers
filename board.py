import pygame
from constants import Constants, Colors
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.setup_board()

    def setup_board(self):
        for row in range(Constants.ROWS):
            self.board.append([])
            for col in range(Constants.COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, Colors.LIGHT_BROWN))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, Colors.DARK_BROWN))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_squares(self, surface):
        surface.fill(Colors.BLACK)
        for row in range(Constants.ROWS):
            for col in range(row % 2, Constants.COLS, 2):
                pygame.draw.rect(surface, Colors.WHITE, 
                                 (col * Constants.SQUARE_SIZE, row * Constants.SQUARE_SIZE, 
                                  Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))

    def draw(self, surface):
        self.draw_squares(surface)
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(surface)
