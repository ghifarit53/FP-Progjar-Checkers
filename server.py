import socket
import threading
import pickle

class CheckersServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print("Server started, waiting for connections...")
        self.connections = []
        self.game_state = None  # Placeholder for game state

    def handle_client(self, conn, player_id):
        conn.send(pickle.dumps({'player_id': player_id}))
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                data = pickle.loads(data)
                self.broadcast(data, conn)
            except Exception as e:
                print(f"Error: {e}")
                break
        conn.close()

    def broadcast(self, data, conn):
        for client in self.connections:
            if client != conn:
                try:
                    client.send(pickle.dumps(data))
                except:
                    client.close()
                    self.connections.remove(client)

    def run(self):
        player_id = 0
        while True:
            conn, addr = self.server.accept()
            print(f"Connected by {addr}")
            self.connections.append(conn)
            threading.Thread(target=self.handle_client, args=(conn, player_id)).start()
            player_id += 1

if __name__ == "__main__":
    server = CheckersServer()
    server.run()
