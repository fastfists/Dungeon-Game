''' Contains Dungeon object and Room objects '''
from tkinter import Tk,Canvas
import random
debug =[]
class dungeon:
    notnull = []
    allrooms = []
    currenType = -1

    def __init__(self ,resolution = 10, roomCount = 3, specialWeigth = 2 , prngnum = random.randint(0,879190747)):
        self.prngNum = prngnum
        self.num = self.prngNum
        self.resolution = resolution
        self.roomCount = roomCount
        self.cantouch = [[0 for _ in range(self.resolution)] for _ in range(self.resolution) ]
        self.Idtbl = [[0 for _ in range(self.resolution)] for _ in range(self.resolution)]
        self.weight = specialWeigth

    def _Prng(self,limit, wantBool = False):
        self.prngNum = (self.prngNum * 154687469+879190747) % 67280421310721
        if wantBool:
            return self.prngNum % limit == 0
        else:
            pass
        return self.prngNum % limit

    def __repr__(self):
        return "Dungeon: {0} , {1}" .format(self.resolution, len(self.allrooms))

    def make(self):
        while True:
            x,y = self._Prng(len(self.Idtbl)), self._Prng(len(self.Idtbl))
            if self._format(3,x,y):
                self.allrooms.append(Room(3, self.currenType,x,y,self.notnull, self.Idtbl))
                break
        while len(self.allrooms) != self.roomCount:
            self.works = False
            x,y = self.notnull[ self._Prng(len(self.notnull)) ]
            moveX , moveY = self.__findDir( self._Prng(4) )
            newX , newY = x + moveX , y + moveY
            try:
                if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0:
                    if self._Prng(self.weight,wantBool=True):
                        size = (4,2)
                        self.weight *= 8
                    elif self.Idtbl[x][y] == 2:
                        size = 4
                    elif self.Idtbl[x][y] == 3 or self.Idtbl[x][y] == 4:
                        size = 2
                    if self._format(size, newX,newY):
                        self.allrooms.append(Room(size, self.currenType,newX, newY , self.notnull, self.Idtbl))
                        newX , newY = self.__startVal(self.allrooms[ len(self.allrooms) - 1 ])
                        self.update(size, self.currenType,newX, newY)
                        # dont forget doors.
            except:
                continue
        self.addWalls()

    def addRoom(self):
        self.removeWalls()
        self.roomCount += 1
        while len(self.allrooms) != self.roomCount:
            self.works = False
            x,y = self.notnull[ self._Prng(len(self.notnull)) ]
            moveX , moveY = self.__findDir( self._Prng(4) )
            newX , newY = x + moveX , y + moveY
            try:
                if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0:
                    if self._Prng(self.weight,wantBool=True):
                        size = (4,2)
                        self.weight *= 8
                    elif self.Idtbl[x][y] == 2:
                        size = 4
                    elif self.Idtbl[x][y] == 3 or self.Idtbl[x][y] == 4:
                        size = 2
                    if self._format(size, newX,newY):
                        self.allrooms.append(Room(size, self.currenType,newX, newY , self.notnull, self.Idtbl))
                        newX , newY = self.__startVal(self.allrooms[ len(self.allrooms) - 1 ])
                        self.update(size, self.currenType,newX, newY)
            except:
                pass
                        
    def __startVal(self, room):
        startVal = 0
        for section in room.blocks:
            for x,y in section:
                if startVal > x + y:
                    startVal = x + y
        return startVal


    def newDraw(self):
        for room in self.allrooms:
            room.draw()

    def draw(self):
        master = Tk()
        dungeon= Canvas(master,width=700,height=700)
        for y in range(self.resolution):
            for x in range (self.resolution):
                w=1
                o='black'
                try:
                    ide = self.Idtbl[x][y] % 5
                except:
                    self.Idtbl[x][y] = 5
                    ide = 5
                if ide == 0:
                    f= 'gray'
                elif ide == 1:
                    f= 'black'
                elif ide == 2:
                    f = 'blue'
                elif ide == 3:
                    f= 'green'
                elif ide == 4:
                    f='purple'
                elif ide ==5:
                    f= 'red'
                if self.Idtbl[x][y] > 5:
                    o='brown'
                    w=1
                dungeon.create_rectangle(x*(700//self.resolution),(y*(700//self.resolution)),((x+1)*(700//self.resolution))-1,((y+1)*(700//self.resolution))-1,fill=f,outline=o,width=w)
                dungeon.pack()
        master.mainloop()

    def _format(self,size, sx,sy):
        ''' Recieves a x and y position and creates the type needed to create it '''
        try:
            width, height = size
        except:
            width,height = size,size
        for typ in range(4):
            works= True
            for y in range(height):
                for x in range(width):
                    if typ == 0:
                        newX,newY = sx+x,sy+y
                    elif typ == 1:
                        newX,newY = sx-x,sy+y
                    elif typ == 2:
                        newX, newY = sx-x, sy-y
                    elif typ == 3:
                        newX,newY = sx+x,sy-y
                    else:
                        return False
                    try:
                        if self.Idtbl[newX][newY] != 0:
                            works = False
                            break
                    except:
                        works=False
                        break
                    if (newX,newY) in self.notnull  or newX < 0 or newY<0:
                        works = False
                        break #breaks from X loop
                if not works:
                    break
            if works:
                self.currenType = typ
                return works
        return False  # returns False because none of the types work

    def update(self, size, how, startX, startY):
        for y in range(startY + 2):
            for x in range(startX + 2):
                _pass = True
                for d in range(4):
                    dirX, dirY = self.__findDir(d)
                    neighborX, neighborY= dirX + x, dirY + y
                    try:
                        self.Idtbl[neighborX][neighborY]
                    except:
                        _pass=False
                        break
                    if (neighborX,neighborY) not in self.notnull:
                        _pass=False
                        break
                if _pass == True and self.cantouch[x][y]==0:
                    try:
                        self.cantouch[x][y]=1
                        self.notnull.remove((x,y))
                    except:
                        pass
    @staticmethod
    def __findDir(dir_index):
        ''' A more conventional method to find the x and y positions '''
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

    def doors(self):
        #TODO add this later in a better way(mabey as a Room method)
        pass

    def addWalls(self):
        checkVals = [x for x in self.notnull if self.cantouch[  x[0] ][  x[1]  ] != 1]
        for tup in checkVals:
            x,y = tup
            for direction in range(8):
                nx,ny = self.__findDir(direction)
                neighborX, neighborY = nx+x, ny+y
                try:
                    if self.Idtbl[neighborX][neighborY] == 0 and neighborX >= 0 and neighborY >= 0:
                        self.Idtbl[neighborX][neighborY] = 1
                        self.notnull.append(neighborX, neighborY)
                except:
                    pass

    def removeWalls(self):
        checkVals = [x for x in self.notnull if self.Idtbl[[ x[0] ][ x[1] ] == 1 ]]
        for tup in checkVals:
            for x,y in tup:
                self.Idtbl[x][y] = 0


class Room:
    ''' A class that contains its own pair of blocks and monsters'''
    def __init__(self, size, how, sx,sy, notnull, idtbl):
        try:
            self.width,self.height = size
        except:
            self.width,self.height = size,size
        if how == 0:
            self.blocks = [Tile(self, size, (sx + x , sy + y) ) for y in range(self.height) for x in range(self.width)]
            print('hi')
        elif how == 1:
            self.blocks = [Tile(self , size, (sx - x , sy + y )) for y in range(self.height) for x in range(self.width)]
        elif how == 2:
            self.blocks = [Tile(self, size , (sx - x , sy - y )) for y in range(self.height) for x in range(self.width)]
        elif how == 3:
            self.blocks = [Tile(self, size, (sx + x , sy - y )) for y in range(self.height) for x in range(self.width)]
        #self.blocks.sort()
        for tile in self.blocks:
            print(tile)
            x,y = tile.position
            print(x,y)
            notnull.append((x,y))
            idtbl[x][y] = size

    def draw(self, resolution):
        pass

    def __repr__(self):
        return "Room: {},{}".format(self.width, self.height)

    def newDoor(self,):
        pass

class Tile:
    def __init__(self, Room, _type, position):
        '''Recieves its room, the type of tile it is, and the X,Y coordinates as a tuple'''
        self.room = Room
        self._type = _type
        self.position = position
        print(self.position)

    def draw(self, resolution):
        pass


if __name__ == "__main__":
    d = dungeon(resolution = 10, roomCount = 5, prngnum=15468746)
    d.make()
    print(d.allrooms.__repr__())
    d.draw()
