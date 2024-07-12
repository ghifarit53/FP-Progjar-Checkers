import socket
import threading
import pickle
from constants import Colors
from board import Board

class GameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.board = Board()
        self.turn = Colors.SADDLEBROWN
        self.lock = threading.Lock()
        self.player_count = 0

    def handle_client(self, conn, addr):
        self.lock.acquire()
        player_number = self.player_count
        self.player_count += 1
        self.lock.release()

        print(f"New connection from {addr} as Player {player_number + 1}")
        conn.send(pickle.dumps(player_number))
        self.clients.append((conn, player_number))

        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                move = pickle.loads(data)
                with self.lock:
                    if self.board.handle_click(move, self.turn):
                        self.turn = Colors.WHITE if self.turn == Colors.SADDLEBROWN else Colors.SADDLEBROWN
                        for client, _ in self.clients:
                            client.sendall(pickle.dumps((self.board, self.turn)))

            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                break

        conn.close()
        self.clients.remove((conn, player_number))

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(2)
        print("Server started, waiting for connections...")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    server = GameServer('localhost', 5555)
    server.start()