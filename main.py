import pygame
import os
import socket
import pickle
from constants import Constants, Colors
from board import Board
from menu import draw_menu

class GameClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.board = None
        self.turn = None

    def send_move(self, move):
        self.client.sendall(pickle.dumps(move))

    def receive_update(self):
        data = self.client.recv(1024)
        return pickle.loads(data)

def main():
    pygame.init()
    aspect_ratio = Constants.WIDTH / Constants.HEIGHT
    min_width, min_height = 600, 600
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Checkers')

    # Load monospace font
    font_path = os.path.join('assets', 'fonts', 'audiowide-mono', 'Audiowide-Mono-Latest.ttf')
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"No file '{font_path}' found in working directory '{os.getcwd()}'")
    font = pygame.font.Font(font_path, 23)

    # Connect to server
    client = GameClient('localhost', 5555)
    board = Board()
    clock = pygame.time.Clock()
    running = True
    menu_active = True
    game_mode = None

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                new_width = max(event.w, min_width)
                new_height = max(event.h, min_height)
                if new_width / new_height > aspect_ratio:
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_height = int(new_width / aspect_ratio)
                surface = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

            if menu_active:
                draw_menu(surface, font)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pvp_button = pygame.Rect(Constants.WIDTH // 4, Constants.HEIGHT // 2, Constants.WIDTH // 2, 50)
                    if pvp_button.collidepoint(pos):
                        menu_active = False
                        game_mode = "pvp"

            if not menu_active and game_mode == "pvp":
                surface.fill(Colors.BLACK)
                board.draw(surface)
                pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        if board.handle_click(pos, client.turn):  # Pass current player's turn
                            client.send_move((board.selected_piece, pos))  # Send move to server

        if not menu_active:
            board_state, client.turn = client.receive_update()  # Update board and turn from server
            board.board = board_state
            board.draw(surface)
            pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
