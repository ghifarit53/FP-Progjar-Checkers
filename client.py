# client.py
import pygame
import socket
import pickle
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

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.board = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return pickle.loads(self.client.recv(4096))

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)

def main():
    pygame.init()
    WIN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    pygame.display.set_caption('Checkers')

    running = True
    in_menu = True
    n = Network()
    board = n.board
    clock = pygame.time.Clock()
    winner = None

    while running:
        if in_menu:
            text_rect = draw_menu(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if in_menu and event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    in_menu = False
                    print("Starting the game...")

            if not in_menu and event.type == pygame.MOUSEBUTTONDOWN and not winner:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if board:
                    if board.handle_click(pos, board.turn):
                        board.turn = Colors.WHITE if board.turn == Colors.SADDLEBROWN else Colors.SADDLEBROWN
                        n.send(board)

            if not in_menu and board and not winner:
                WIN.fill(Colors.BLACK)
                board.draw(WIN)
                winner = board.winner()
                pygame.display.flip()

                board = n.send(board)
                winner = board.winner()

        if winner:
            display_winner(WIN, 'Brown' if winner == Colors.SADDLEBROWN else 'White')
            running = False

        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
