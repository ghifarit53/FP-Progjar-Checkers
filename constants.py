# constants.py

class Constants:
    WIDTH = 600
    HEIGHT = 600
    ROWS = 8
    COLS = 8
    SQUARE_SIZE = WIDTH // COLS         # Size of each square on the board

class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_BROWN = (210, 180, 140)
    DARK_SQUARE = (101, 67, 33)
    LIGHT_SQUARE = (245, 245, 245)  # Lighter color for the light squares
    HIGHLIGHT = (255, 255, 0)  # Highlight color for pieces
    MENU_BG = (30, 30, 30)  # Menu background color
    BUTTON_COLOR = (0, 200, 200)  # Button color
    TEXT_COLOR = (255, 255, 255)  # Text color