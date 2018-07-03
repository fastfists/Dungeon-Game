import socket
import time
import sys

def init():
    global host, port, sock, ending, clients
    host = "127.0.0.1"
    port = 9000

    clients = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.setblocking(0)

    inited = True
    ending = False
    print("Server Ready")

map_data = [[4,1],
            [2,3]]

def run():
    global ending
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
            end()
        except KeyboardInterrupt:
            end()
        except SyntaxError as e:
            raise e
        except OSError:
            pass

def if_running(func):
    def wrapped(*args, **kwargs):
        if not ending:
            return func(*args, **kwargs)
    return wrapped

@if_running
def end():
    global ending
    print("closing connection")
    ending = True
    sock.close()

def execute():
    init()
    run()
    end()
    sys.exit()

if __name__ == '__main__':
    execute()
