# board.py
import pygame
from constants import Constants, Colors
from piece import Piece

class Board:
    def __init__(self):
        self.board = []  # 2D list to store pieces
        self.selected_piece = None  # Track selected piece
        self.valid_moves = []  # Track valid moves for the selected piece
        self.setup_board()

    def setup_board(self):
        # Set up the initial board configuration with pieces
        for row in range(Constants.ROWS):
            self.board.append([])
            for col in range(Constants.COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, Colors.WHITE))  # Add light pieces
                    elif row > 4:
                        self.board[row].append(Piece(row, col, Colors.BLACK))  # Add black pieces
                    else:
                        self.board[row].append(0)  # Empty square
                else:
                    self.board[row].append(0)  # Empty square

    def draw(self, surface):
        width, height = surface.get_size()
        square_size = min(width // Constants.COLS, height // Constants.ROWS)
        surface.fill(Colors.BLACK)

        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                rect = (col * square_size, row * square_size, square_size, square_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(surface, Colors.LIGHT_SQUARE, rect)
                else:
                    pygame.draw.rect(surface, Colors.DARK_SQUARE, rect)

        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(surface, square_size)

        if self.selected_piece is not None:
            row, col = self.selected_piece
            pygame.draw.rect(surface, Colors.HIGHLIGHT, (col * square_size, row * square_size, square_size, square_size), 4)
            for move in self.valid_moves:
                row, col = move
                pygame.draw.circle(surface, Colors.HIGHLIGHT, (col * square_size + square_size // 2, row * square_size + square_size // 2), 15)

    def handle_click(self, pos):
        row = pos[1] // (Constants.HEIGHT // Constants.ROWS)
        col = pos[0] // (Constants.WIDTH // Constants.COLS)

        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece, (row, col))
                self.selected_piece = None
                self.valid_moves = []
                return True
            else:
                self.selected_piece = None
                self.valid_moves = []
        else:
            piece = self.board[row][col]
            if piece != 0:
                self.selected_piece = (row, col)
                self.valid_moves = piece.get_valid_moves(self.board)
        return False

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = 0
        self.board[end_row][end_col].move(end_row, end_col)

        # Promote to king if reaching the opposite end
        if end_row == 0 or end_row == Constants.ROWS - 1:
            self.board[end_row][end_col].make_king()
