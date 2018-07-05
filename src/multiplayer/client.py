import socket
import numpy as np
import tkinter as tk
import json

def draw(data):
    """
    Draws data recieved from the connect
    """
    master = tk.Tk()
    data = np.array(data)
    dungeon = tk.Canvas(master,width=700,height=700)
    print(data)
    print(data.shape)
    resolution = data.shape[0]

    for y in range(resolution):
        for x in range(resolution):
            w = 1
            o = 'black'
            ide = data[x][y]
            if ide == 0:
                f = 'gray'
            elif ide == 1:
                f = 'black'
            elif ide == 2:
                f = 'blue'
            elif ide == 3:
                f = 'green'
            elif ide == 4:
                f = 'purple'
            else:
                f = 'orange'
            dungeon.create_rectangle(
                                    x*(700//resolution),
                                    (y*(700//resolution)),
                                    ((x+1)*(700//resolution))-1,
                                    ((y+1)*(700//resolution))-1,
                                    fill=f,
                                    outline=o,
                                    )
            dungeon.pack()
    master.mainloop()    

def init(_host = socket.gethostname(), _port=0 , _server: tuple=None):
    global host, port, server
    host = "127.0.0.1"
    port = 0
    server = _server

def set_server(_server):
    global server
    server = _server

def request(_request:str):
    def get_resource(sock: socket.socket):
        while True:
            try:
                resource, addr = sock.recvfrom(1024)
                if resource:
                    break
            except:
                pass
        return resource

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        global host, port, server
        sock.bind((host, port))
        sock.setblocking(0)
        sock.sendto(bytes(thing, "utf-8"), server)
        print(f"bound to port {port}")
        resource = get_resource(sock).decode("utf-8").replace("'",'"')
        resource = json.loads(resource)[_request]
        #time.sleep(0.2)
    return resource

def execute():
    init()
    map_data = request("map")
    print(map_data)
    draw(map_data["map"])

if __name__ == '__main__':
    execute()