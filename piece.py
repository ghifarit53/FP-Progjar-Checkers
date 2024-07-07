import pygame
from constants import Constants, Colors

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.is_king = False
        self.calculate_pos()

    def calculate_pos(self):
        self.x = Constants.SQUARE_SIZE * self.col + Constants.SQUARE_SIZE // 2
        self.y = Constants.SQUARE_SIZE * self.row + Constants.SQUARE_SIZE // 2

    def draw(self, surface, square_size):
        radius = square_size // 2 - 10
        pygame.draw.circle(surface, Colors.GREEN, (self.x, self.y), radius + 2)
        pygame.draw.circle(surface, self.color, (self.x, self.y), radius)
        if self.is_king:
            crown_img = pygame.image.load('assets/images/crown.png')
            crown_img = pygame.transform.scale(crown_img, (square_size, square_size))
            surface.blit(crown_img, (self.x - square_size // 2, self.y - square_size // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_pos()

    def make_king(self):
        self.is_king = True

    def get_valid_moves(self, board):
        valid_moves = []
        directions = []
        if self.color == Colors.BLACK:
            directions = [(-1, -1), (-1, 1)]
        elif self.color == Colors.WHITE:
            directions = [(1, -1), (1, 1)]
        if self.is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            dir_row, dir_col = direction
            new_row = self.row + dir_row
            new_col = self.col + dir_col

            if 0 <= new_row < Constants.ROWS and 0 <= new_col < Constants.COLS:
                if board[new_row][new_col] == 0:
                    valid_moves.append((new_row, new_col))
                elif board[new_row][new_col].color != self.color:
                    jump_row = new_row + dir_row
                    jump_col = new_col + dir_col
                    if 0 <= jump_row < Constants.ROWS and 0 <= jump_col < Constants.COLS:
                        if board[jump_row][jump_col] == 0:
                            valid_moves.append((jump_row, jump_col))

        return valid_moves