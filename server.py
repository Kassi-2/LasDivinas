import socket
import threading

server = "localhost"
port = 5050
server_ip = socket.gethostbyname(server)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip, port))
s.listen(2)
print("Esperando conexión...")

pos = ["0:50,50", "1:100,100"]

def threaded_client(conn, player_id):
    conn.send(str.encode(player_id))
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            pos[int(player_id)] = data.decode('utf-8')
            player2_id = 1 - int(player_id)
            conn.sendall(str.encode(pos[player2_id]))
        except:
            break
    conn.close()

current_id = 0
while True:
    conn, addr = s.accept()
    print(f"Conectado a: {addr}")
    threading.Thread(target=threaded_client, args=(conn, str(current_id))).start()
    current_id = 1 - current_id