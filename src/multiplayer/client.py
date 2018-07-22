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

def init(_host = socket.gethostname(), _port=0 , _host_server: tuple=None):
    global host, port, host_server
    host = _host
    port = _port
    host_server = _host_server 
    if host_server is None:
        host_server = (host, 9000)

def set_host_server(_host_server):
    global host_server
    host_server = _host_server

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
        global host, port, host_server
        sock.bind((host, port))
        sock.setblocking(0)
        sock.sendto(bytes(_request, "utf-8"), host_server)
        print(f"bound to port {port}")
        resource = get_resource(sock).decode("utf-8").replace("'",'"')
        print(f"resource is: {resource}, type: {type(resource)}")
        resource = json.loads(resource)
        print(f"Resource now is {resource}, type: {type(resource)}")
        #time.sleep(0.2)
    return resource

def execute():
    init()
    map_data = request("map")
    draw(map_data["map"])

if __name__ == '__main__':
    execute()