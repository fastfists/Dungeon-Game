""" The old dungeon """

from tkinter import Tk,Canvas
import math
g=0

prngNum = int(input("What is the seed? "))
resolution = int(input('What is the resolution (10 is recommended): '))
roomamt= int(input("how many rooms? "))
Idtbl=[[0 for i in range(resolution)] for i in range(resolution)]
cantouch=[[0 for i in range(resolution)] for i in range(resolution)]
notnull=[]
allrooms=[]
master= Tk()
dungeon= Canvas(master,width=1000,height=1000)
def Prng(limit):
    global prngNum
    prngNum = (prngNum*154687469+879190747) % 67280421310721
    return prngNum % limit

def find_dir(dir_index):
    if dir_index==0:
        return (1,0)
    if dir_index== 1:
        return (-1,0)
    if dir_index== 2:
        return (0,1)
    if dir_index== 3:
        return (0,-1)
    if dir_index == 4:
        return (-1,-1)
    if dir_index == 5:
        return (1,-1)
    if dir_index == 6:
        return (-1,1)
    if dir_index == 7:
        return (1,1)
    
def setup():
    """
    pn in the Seed
    r is the Resoluion
    rm is the room ammount
    """
    global prngNum, resolution, roomamt, Idtbl, cantouch, allrooms, master, dungeon, notnull

    Idtbl=[[0 for i in range(resolution)] for i in range(resolution)]
    cantouch=[[0 for i in range(resolution)] for i in range(resolution)]
    notnull=[]
    allrooms=[]
    master= Tk()
    dungeon= Canvas(master,width=1000,height=1000)
    dungeon_master()    


def dungeon_master():
    """The main man stan that controls the map"""
    while True:
        x = Prng(len(Idtbl))
        y= Prng(len(Idtbl))
        works, typ=format(3, x, y)
        if works == True:
            allrooms.append(Room(3, typ, x, y))
            break
    while True:
        works = False
        """repats until all the rooms needed are created"""
        if len(allrooms) == roomamt:
            break
        moveX,moveY=find_dir( Prng(4) )
        Xpos, Ypos = notnull[ Prng(len(notnull)) ]
        newX, newY = Xpos+moveX, Ypos+moveY
        """creates either a trap room or a boss room"""
        try:
            Idtbl[newX][newY]
        except:
            pass
        else:
            if Idtbl[newX][newY]==0 and cantouch[Xpos][Ypos] == 0:
                if Idtbl[Xpos][Ypos] == 2:
                    size = 4
                    works, typ = format(size, newX, newY)
                if Idtbl[Xpos][Ypos] == 3 or Idtbl[Xpos][Ypos] == 4:
                    size = 2
                    works, typ = format(size, newX,newY)
                if works == True:
                    allrooms.append(Room(size, typ, newX,newY))
                    newdoor(Xpos, Ypos) # adds a new door at the starting values of the place made
                    newdoor(newX, newY) # adds a new door at the new values so they can be connected
                    
    walls()
    draw()




def format(size, sx ,sy):
    global g
    for typ in range(4):
        works= True
        for y in range(size):
            for x in range(size):
                """sets a new postion for the room to check all values in the room"""
                if typ == 0:
                    newX,newY= sx+x, sy+y
                if typ == 1:
                    newX,newY= sx-x, sy+y
                if typ == 2:
                    newX,newY= sx-x, sy-y
                if typ == 3:
                    newX,newY= sx+x, sy-y
                """Checks if that new values is illegal"""
                try:
                    if Idtbl[newX][newY] != 0:
                        works=False
                except:
                    works=False
                    break
                if (newX,newY) in notnull  or newX < 0 or newY<0  or not works:
                    works= False
                    break #breaks from X loop
        if works:
            return(works,typ)  
    return (False, typ)  # returns False because none of the types work
    
def newdoor(doorX, doorY):
    for i in allrooms:
        try:
            i.blocks.index((doorX,doorY))
        except:
            pass
        else:
            i.door_count+=1
            Idtbl[doorX][doorY] += 5
            break
    


def update():
    for y in range(resolution):
        for x in range(resolution):
            pas = True
            for d in range(4):
                dirX, dirY = find_dir(d)
                neighborX, neighborY= dirX + x, dirY + y
                try:
                    Idtbl[neighborX][neighborY]
                except:
                    pas=False
                    break
                if (neighborX,neighborY) not in notnull:
                    pas=False
                    break
            if pas== True and cantouch[x][y]==0:
                try:
                    cantouch[x][y]=1
                    notnull.remove((x,y))
                except:
                    pass
                    
def draw():
        dungeon = Canvas(master,width=700,height=700)
        for y in range(resolution):
            for x in range(resolution):
                w = 1
                o = 'black'
                ide = Idtbl[x][y] % 5
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
                if Idtbl[x][y] > 5:
                    o = 'brown'
                dungeon.create_rectangle(
                                        x*(700//resolution),
                                        (y*(700//resolution)),
                                        ((x+1)*(700//resolution))-1,
                                        ((y+1)*(700//resolution))-1,
                                        fill=f,
                                        outline=o,
                                        width=w
                                        )
                dungeon.pack()
        master.mainloop()


def walls():
    for y in range(resolution):
        for x in range(resolution):
            if (x,y) in notnull:
                for direction in range(8):
                    nx,ny = find_dir(direction)
                    neighborX, neighborY = nx+x, ny+y
                    try:
                        if Idtbl[neighborX][neighborY]== 0 and neighborX>=0 and neighborY>=0:
                            Idtbl[neighborX][neighborY]=1 
                    except:
                        pass
class Room:
    def __init__(self,size,how,sx,sy):
        self.size= size
        self.blocks=[]
        self.door_count =0
        if size != 3:
            self.monsters= Prng(3)
        else:
            self.monsters= 4  #special code for the boss
        for y in range(size):
            for x in range(size):
                if how == 0:
                    newX,newY= sx+x, sy+y
                if how == 1:
                    newX,newY= sx-x, sy+y
                if how == 2:
                    newX,newY= sx-x, sy-y
                if how == 3:
                    newX,newY= sx+x, sy-y
                packedpos=(newX,newY)
                Idtbl[newX][newY]=size
                notnull.append(packedpos)                
                self.blocks.append(packedpos)
        update()
    def showMonsters(self):
        pass
    def ison(self):
        pass

if __name__=='__main__':
    print('peek')
    setup()
