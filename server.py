# server.py
import socket
import pickle
from _thread import start_new_thread
from board import Board

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
id_count = 0

def threaded_client(conn, player, game_id):
    global id_count
    conn.send(pickle.dumps((game_id, player)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    game = data

                games[game_id] = game

                if game.winner():
                    print(f"Game {game_id} has a winner: {game.winner()}")
                
                reply = game
                conn.sendall(pickle.dumps(reply))
            else:
                break
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass
    id_count -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_count += 1
    player = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Board()
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        player = 1

    start_new_thread(threaded_client, (conn, player, game_id))
