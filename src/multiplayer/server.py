import socket


def Main():
    host = ''
    port = 5050

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()
    print("Connection from:", addr)
    while True:
        data = c.recv(1024)
        if not data:
            break
        print("from connected user: ", data)
        data = data.decode("utf-8").upper()
        print("sending: ", data)
        c.send(str.encode(data))
    c.close()

if __name__ == '__main__':
    Main()
