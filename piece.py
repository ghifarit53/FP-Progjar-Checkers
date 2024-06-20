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
        self.calc_position()

    def calc_position(self):
        self.x = Constants.SQUARE_SIZE * self.col + Constants.SQUARE_SIZE // 2
        self.y = Constants.SQUARE_SIZE * self.row + Constants.SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, surface):
        radius = Constants.SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(surface, Colors.HIGHLIGHT, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(surface, self.color, (self.x, self.y), radius)
        if self.king:
            pygame.draw.circle(surface, Colors.WHITE, (self.x, self.y), radius // 2)

    def __repr__(self):
        return str(self.color)
