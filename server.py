import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "0.0.0.0" #??????revisar
port= 5050
server_ip = socket.gethostbyname(server)
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Esperando conexión...")

currentId = "0"
pos = ["0:50,50", "1:100,100"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply= ''
    while True:
        try:
            data= conn.recv(1024)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Chaooo"))
                break
            else:
                print("Recieved"+ reply)
                arr=reply.split(":")
                id = int(arr[0])
                pos[id]=reply

                if id == 0: nid=1
                if id == 1: nid=0
                reply = pos[nid][:]
                print("Sending: " + reply)
                conn.sendall(str.encode(reply))
        except:
            break
