import pygame
from constants import Constants, Colors
from piece import Piece

class Board:
    def __init__(self):
        self.board = []  # 2D list to store pieces
        self.selected_piece = None
        self.current_turn = Colors.LIGHT_BROWN
        self.setup_board()
        self.font = pygame.font.Font(None, 36)
        self.quit_button_rect = pygame.Rect(Constants.WIDTH - 180, 500, 160, 50)

    def setup_board(self):
        for row in range(Constants.ROWS):
            self.board.append([])
            for col in range(Constants.COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, Colors.LIGHT_BROWN))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, Colors.BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, surface):
        width, height = surface.get_size()
        square_size = Constants.SQUARE_SIZE
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

        self.draw_ui(surface)

    def draw_ui(self, surface):
        # Draw the current turn display
        turn_text = "Turn: Light Brown" if self.current_turn == Colors.LIGHT_BROWN else "Turn: Black"
        turn_surface = self.font.render(turn_text, True, Colors.WHITE)
        surface.blit(turn_surface, (Constants.WIDTH - 180, 50))

        # Draw the quit button
        pygame.draw.rect(surface, Colors.RED, self.quit_button_rect)
        quit_text = self.font.render("Quit Game", True, Colors.WHITE)
        quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
        surface.blit(quit_text, quit_text_rect)

    def select_piece(self, row, col):
        if self.board[row][col] != 0 and self.board[row][col].color == self.current_turn:
            self.selected_piece = self.board[row][col]
            return True
        return False

    def move_piece(self, row, col):
        if self.selected_piece:
            self.board[self.selected_piece.row][self.selected_piece.col] = 0
            self.selected_piece.row = row
            self.selected_piece.col = col
            self.board[row][col] = self.selected_piece
            self.selected_piece = None
            self.switch_turn()

    def switch_turn(self):
        self.current_turn = Colors.BLACK if self.current_turn == Colors.LIGHT_BROWN else Colors.LIGHT_BROWN

    def handle_click(self, pos, surface):
        if self.quit_button_rect.collidepoint(pos):
            return "QUIT"

        width, height = surface.get_size()
        square_size = Constants.SQUARE_SIZE
        row, col = pos[1] // square_size, pos[0] // square_size
        if self.selected_piece:
            self.move_piece(row, col)
        else:
            self.select_piece(row, col)
        return None

    def get_game_state(self):
        return [[piece.color if piece != 0 else 0 for piece in row] for row in self.board]

    def update_game_state(self, state):
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                if state[row][col] == 0:
                    self.board[row][col] = 0
                else:
                    color = state[row][col]
                    self.board[row][col] = Piece(row, col, color)
