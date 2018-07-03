import socket
import time

host = "127.0.0.1"
port = 8081

clients = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
sock.setblocking(0)

ending = False
print("Server Ready")

map_data = [[4,1],
            [2,3]]

while not ending:
    try:
        data, addr = sock.recvfrom(1024)
        print(f"Recieved request for {data.decode('utf-8')}")
        if addr not in clients:
            clients.append(addr)
        if data.decode('utf-8') == "map":
            return_val = bytes(str(map_data), "utf-8")
        print(f"sending out data {data} to {addr}: ({return_val})")
        for client in clients:
            sock.sendto(return_val, client)

        ending = True
    except:
        pass

sock.close()
