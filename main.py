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
        self.board = Board()
        self.player_id = None
        self.current_player = None

    def start(self):
        data = self.client.recv(1024)
        self.player_id = pickle.loads(data)
        print(f"You are Player {self.player_id + 1}")

    def send_move(self, move):
        self.client.sendall(pickle.dumps(move))

    def receive_update(self):
        data = self.client.recv(1024)
        board_state, self.current_player = pickle.loads(data)
        self.board.board = board_state
        return self.board, self.current_player

def main():
    pygame.init()
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    pygame.display.set_caption('Checkers 101')

    font_path = os.path.join('assets', 'fonts', 'audiowide-mono', 'Audiowide-Mono-Latest.ttf')
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"No file '{font_path}' found in working directory '{os.getcwd()}'")
    font = pygame.font.Font(font_path, 23)

    client = GameClient('localhost', 5555)
    client.start()

    clock = pygame.time.Clock()
    running = True
    menu_active = True
    game_mode = None

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if menu_active:
                draw_menu(surface, font)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    button_rect = pygame.Rect((Constants.WIDTH - (font.size('Checkers 101')[0] + 40)) // 2, Constants.HEIGHT // 2, font.size('Checkers 101')[0] + 40, font.size(' P v P ')[1] + 20)
                    if button_rect.collidepoint(pos):
                        menu_active = False
                        game_mode = "pvp"
            if not menu_active and game_mode == "pvp":
                surface.fill(Colors.BLACK)
                client.board.draw(surface)
                pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN and client.current_player == client.player_id:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        if client.board.handle_click(pos, "player1" if client.player_id == 0 else "player2"):
                            client.send_move((client.board.selected_piece, pos))

        if not menu_active:
            client.board, client.current_player = client.receive_update()
            client.board.draw(surface)
            pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()