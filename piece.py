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
        self.calculate_position()

    def calculate_position(self, square_size=Constants.SQUARE_SIZE):
        self.x = self.col * square_size + square_size // 2
        self.y = self.row * square_size + square_size // 2

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()

    def draw(self, surface, square_size):
        self.calculate_position(square_size)
        radius = max(square_size // 2 - self.PADDING, 8)
        pygame.draw.circle(surface, Colors.HIGHLIGHT, (self.x, self.y), radius + self.OUTLINE)  
        pygame.draw.circle(surface, self.color, (self.x, self.y), radius) 
        if self.king:
            pygame.draw.circle(surface, Colors.WHITE, (self.x, self.y), radius // 2)  

    def __repr__(self):
        return str(self.color)  
