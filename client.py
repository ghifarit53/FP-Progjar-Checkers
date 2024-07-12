import pygame
from board import Board
from constants import Colors, Constants

FPS = 60

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // Constants.SQUARE_SIZE
    col = x // Constants.SQUARE_SIZE
    return row, col

def draw_menu(win):
    win.fill(Colors.BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render('Play Game', True, Colors.WHITE)
    text_rect = text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2))
    pygame.draw.rect(win, Colors.BLUE, text_rect.inflate(20, 20))
    win.blit(text, text_rect)
    pygame.display.flip()
    return text_rect

def display_winner(win, winner):
    font = pygame.font.Font(None, 74)
    text = font.render(f'The winner is {winner}', True, Colors.WHITE)
    text_rect = text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2))
    pygame.draw.rect(win, Colors.BLACK, text_rect.inflate(20, 20))
    win.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    pygame.init()
    WIN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    pygame.display.set_caption('Checkers')

    running = True
    in_menu = True
    board = None
    winner = None

    while running:
        if in_menu:
            text_rect = draw_menu(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if in_menu and event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    board = Board()
                    in_menu = False

            if not in_menu and event.type == pygame.MOUSEBUTTONDOWN and not winner:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if board:
                    if board.handle_click(pos, board.turn):
                        board.turn = Colors.WHITE if board.turn == Colors.SADDLEBROWN else Colors.SADDLEBROWN

            if not in_menu and board and not winner:
                WIN.fill(Colors.BLACK)
                board.draw(WIN)
                winner = board.winner()
                pygame.display.flip()

        if winner:
            display_winner(WIN, 'Brown' if winner == Colors.SADDLEBROWN else 'White')
            running = False

    pygame.quit()

if __name__ == '__main__':
    main()
