import socket
import time
import sys
import copy

def init(_host = socket.gethostname(), _port=9000):
    global host, port, sock, ending, clients, resources
    host = _host
    port = _port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.setblocking(0)

    clients = []
    resources = dict()
    ending = False
    print("Server Ready")

def run():
    global ending
    while not ending:
        try:
            data, addr = sock.recvfrom(2048)
            print(f"Recieved request for {data.decode('utf-8')}")
            if addr not in clients:
                clients.append(addr)
            resutls = fetch(data.decode("utf-8"))
            return_val = str(resutls).encode()
            print(f"sending out data {data} to {addr}: ({return_val})")
            for client in clients:
                sock.sendto(return_val, client)
            end()
        except KeyboardInterrupt:
            end()
        except OSError:
            pass

def fetch(request: str):
    global resources
    request = request.split()
    results = copy.copy(resources)
    for key in results.keys():
        if key not in request:
            del results[key]
    return results

def add_resources(**kwargs):
    """
    Recieves key, value pairs to add to the resource dictionary
    """
    global resources
    resources.update(kwargs)

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
    add_resources(map=[[2,3], [3,4]])
    run()
    end()
    sys.exit()

if __name__ == '__main__':
    execute()
