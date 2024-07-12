import pygame
from constants import Constants, Colors
from piece import Piece

class Board:
    def __init__(self):
        self.board = []  # 2D list to store pieces
        self.selected_piece = None
        self.turn = Colors.LIGHT_BROWN
        self.valid_moves = {}
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

    def select_piece(self, row, col):
        if self.selected_piece:
            result = self.move(self.selected_piece, row, col)
            if not result:
                self.selected_piece = None
                self.select_piece(row, col)

        piece = self.board[row][col]
        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
        return False

    def move(self, piece, row, col):
        if (row, col) in self.valid_moves:
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)

            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board[skipped.row][skipped.col] = 0

            if row == 0 or row == Constants.ROWS - 1:
                piece.make_king()

            self.change_turn()
            return True
        return False

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == Colors.LIGHT_BROWN or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == Colors.BLACK or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, Constants.ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, Constants.ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, Constants.ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= Constants.COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, Constants.ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == Colors.LIGHT_BROWN:
            self.turn = Colors.BLACK
        else:
            self.turn = Colors.LIGHT_BROWN
