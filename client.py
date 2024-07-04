import pygame
import socket
import pickle
import threading
from constants import Constants
from board import Board
from menu import Menu

class CheckersClient:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.player_id = None
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.start()

    def receive_data(self):
        while True:
            try:
                data = self.client.recv(4096)
                if not data:
                    break
                data = pickle.loads(data)
                self.handle_data(data)
            except Exception as e:
                print(f"Error: {e}")
                break

    def send_data(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except Exception as e:
            print(f"Error: {e}")

    def handle_data(self, data):
        if 'player_id' in data:
            self.player_id = data['player_id']
        else:
            self.game.update_game_state(data)

    def run(self):
        main(self)

def main(client):
    pygame.init()
    aspect_ratio = Constants.WIDTH / Constants.HEIGHT
    min_width, min_height = 300, 300
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Checkers')

    board = Board()
    client.game = board
    menu = Menu()
    clock = pygame.time.Clock()
    running = True
    in_menu = True

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_menu:
                    button_text = menu.get_button(event.pos)
                    if button_text == "Start Game":
                        in_menu = False
                    elif button_text == "Quit":
                        running = False
                else:
                    result = board.handle_click(event.pos, surface)
                    if result == "QUIT":
                        running = False
                    else:
                        client.send_data(board.get_game_state())

            if event.type == pygame.MOUSEMOTION:
                if in_menu:
                    menu.update_hover(event.pos)

        if in_menu:
            menu.draw(surface)
        else:
            board.draw(surface)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    client = CheckersClient()
    client.run()
