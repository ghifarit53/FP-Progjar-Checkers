import socket
import threading
import pickle
from board import Board

class GameServer:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.clients = []
        self.board = Board()
        self.current_player = 0

    def start(self):
        print("Server started. Waiting for players...")
        while len(self.clients) < 2:
            client, addr = self.server.accept()
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client, len(self.clients) - 1)).start()
            print(f"Player {len(self.clients)} connected from {addr}")

        print("Two players connected. Starting the game.")
        self.broadcast_state()

    def handle_client(self, client, player_id):
        client.send(pickle.dumps(player_id))
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                move = pickle.loads(data)
                if self.process_move(move, player_id):
                    self.current_player = 1 - self.current_player
                    self.broadcast_state()
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        self.clients.remove(client)
        client.close()

    def process_move(self, move, player_id):
        if player_id != self.current_player:
            return False
        start_pos, end_pos = move
        return self.board.handle_click(end_pos, "player1" if player_id == 0 else "player2")

    def broadcast_state(self):
        state = (self.board.board, self.current_player)
        for client in self.clients:
            client.sendall(pickle.dumps(state))

if __name__ == "__main__":
    server = GameServer('localhost', 5555)
    server.start()