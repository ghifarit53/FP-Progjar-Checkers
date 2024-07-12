import pygame
import socket
import pickle
import threading
from constants import Constants, Colors
from board import Board

class CheckersClient:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.board = Board()
        self.turn = Colors.LIGHT_BROWN
        self.running = True

    def receive_data(self):
        while self.running:
            try:
                data = self.client.recv(2048)
                if not data:
                    break
                self.board = pickle.loads(data)
            except:
                break

    def send_data(self, board):
        self.client.send(pickle.dumps(board))

    def main(self):
        pygame.init()
        aspect_ratio = Constants.WIDTH / Constants.HEIGHT
        min_width, min_height = 300, 300
        surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Checkers')
        clock = pygame.time.Clock()

        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.turn == Colors.LIGHT_BROWN:  # Update turn as needed
                        x, y = pygame.mouse.get_pos()
                        row, col = y // Constants.SQUARE_SIZE, x // Constants.SQUARE_SIZE
                        if self.board.select_piece(row, col):
                            self.send_data(self.board)
                elif event.type == pygame.VIDEORESIZE:
                    new_width = max(event.w, min_width)
                    new_height = max(event.h, min_height)
                    if new_width / new_height > aspect_ratio:
                        new_width = int(new_height * aspect_ratio)
                    else:
                        new_height = int(new_width / aspect_ratio)
                    surface = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

            self.board.draw(surface)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        self.client.close()

if __name__ == "__main__":
    client = CheckersClient()
    client.main()
