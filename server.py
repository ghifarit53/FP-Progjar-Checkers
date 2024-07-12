import socket
import threading
from board import Board
import pickle

class CheckersServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.board = Board()
        self.clients = []

    def handle_client(self, conn, player):
        conn.send(pickle.dumps(self.board))
        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    break

                board = pickle.loads(data)
                self.board = board
                self.broadcast(board, conn)
            except:
                break

        conn.close()
        self.clients.remove(conn)

    def broadcast(self, board, conn):
        for client in self.clients:
            if client != conn:
                try:
                    client.send(pickle.dumps(board))
                except:
                    client.close()
                    self.clients.remove(client)

    def run(self):
        print('Server started...')
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            print(f'Connected by {addr}')

            player = len(self.clients)
            thread = threading.Thread(target=self.handle_client, args=(conn, player))
            thread.start()

if __name__ == "__main__":
    server = CheckersServer()
    server.run()
