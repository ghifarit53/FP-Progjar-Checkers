import socket
import threading
import pickle

class GameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.board = self.initialize_board()
        self.turn = "player1"

    def initialize_board(self):
        board = []
        for row in range(8):
            board.append([0] * 8)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = "W"  # White pieces for Player 1
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = "B"  # Black pieces for Player 2
        return board

    def handle_client(self, conn, addr):
        print(f"New connection from {addr}")
        self.clients.append(conn)

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                move = pickle.loads(data)
                self.process_move(move)

                for client in self.clients:
                    client.sendall(pickle.dumps((self.board, self.turn)))

            except:
                break

        conn.close()
        self.clients.remove(conn)

    def process_move(self, move):
        start_pos, end_pos = move
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = 0

        if self.turn == "player1":
            self.turn = "player2"
        else:
            self.turn = "player1"

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
