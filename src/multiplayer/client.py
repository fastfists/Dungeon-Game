import socket
import numpy as np


def draw(map):
    map = np.array(map)
    

def Main():
    host = ''
    port = 5050

    s = socket.socket()
    s.connect((host, port))

    message = input("-> ")
    while message != 'q':
        s.send(str.encode(message))
        data = s.recv(1024)
        print('Received from server: ' + str(data))
        message = input("-> ")
    s.close()

if __name__ == '__main__':
    Main()
