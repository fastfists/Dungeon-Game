''' Contains Dungeon object and Room objects '''
from tkinter import Tk, Canvas
import random
try:
    from utils import *
except ImportError: pass
try:
    from game import *
except ImportError: pass 
try:
    import pygame
except ImportError: pass



from characters import Monster, BossMonster




class Dungeon:
    notnull = []
    allrooms = []
    currenType = -1
    '''
    __init__ method:
        - Resolution as a tuple (width,height)
        - Roomcount as an int
    '''
    def __init__(self ,resolution, roomCount, game, specialWeigth = 2 , seed = random.randint(0,879190747)):
        self.game = game
        self.prngNum = seed
        self.seed = self.prngNum
        self.RESOLUTION = resolution
        self.WIDTH, self.HEIGHT = self.RESOLUTION
        self.roomCount = roomCount
        self.cantouch = [[0 for _ in range(self.HEIGHT)] for _ in range(self.WIDTH) ]
        self.Idtbl = [[0 for _ in range(self.HEIGHT)] for _ in range(self.WIDTH)]
        self.weight = specialWeigth
        self.walls = []

    def _Prng(self,limit, wantBool = False):
        self.prngNum = (self.prngNum * 154687469+879190747) % 67280421310721
        if wantBool: return self.prngNum % limit == 0
        else: pass
        return self.prngNum % limit

    def __repr__(self):
        return "Dungeon: {0} , {1}" .format(self.RESOLUTION, len(self.allrooms))

    def make(self):
        works = False
        while not works:
            x,y = self._Prng(len(self.Idtbl)), self._Prng(len(self.Idtbl))
            if self._format(3,x,y):
                self.allrooms.append(Room(3, self.currenType,x,y,self.notnull, self.Idtbl, self,is_boss=True))
                works = True
        while len(self.allrooms) != self.roomCount:
            self.works = False
            x,y = self.notnull[ self._Prng(len(self.notnull)) ]
            moveX , moveY = self.__findDir( self._Prng(4) )
            newX , newY = x + moveX , y + moveY
            try:
                if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0:
                    if self.Idtbl[x][y] != 2:
                        size = 2                    
                    if self._Prng(self.weight,wantBool=True):
                        size = (4,2)
                        self.weight *= 8
                    elif self.Idtbl[x][y] == 2:
                        size = 4
                    if self._format(size, newX,newY):
                        self.allrooms.append(Room(size, self.currenType,newX, newY , self.notnull, self.Idtbl,self))
                        newX , newY = self.__startVal(self.allrooms[ len(self.allrooms) - 1 ])
                        self.update(size, self.currenType,newX, newY)
                        # dont forget doors.
            except IndexError: pass
        self.make_start_pos()
        self.addWalls()

    def addRoom(self):
        self.removeWalls()
        self.roomCount += 1
        while len(self.allrooms) != self.roomCount:
            self.works = False
            x, y = self.notnull[ self._Prng(len(self.notnull)) ]
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
                        self.allrooms.append(Room(size, self.currenType,newX, newY , self.notnull, self.Idtbl,self))
                        newX , newY = self.__startVal(self.allrooms[ len(self.allrooms) - 1 ])
                        self.update(size, self.currenType,newX, newY)
            except: continue

    @staticmethod           
    def __startVal(room):
        startVal = (0,0)
        for section in room.blocks:
            x,y = section.position
            if startVal < (x, y): startVal = (x, y)
        return startVal


    def _draw(self, tilesize=32):
        if  self.game is None:
            self.__draw(32)
        for room in self.allrooms:
            room.room_draw()
        self.start_room.room_draw()
        for wall in self.walls:
            wall.draw()

    def __draw(self,tilesize):
        ''' This is Deprocated '''
        self.master = Tk()
        dungeon= Canvas(self.master,width=self.WIDTH*tilesize,height=self.HEIGHT*tilesize)
        for y in range(self.HEIGHT):
            for x in range (self.WIDTH):
                w=1
                o='black'
                ide = self.Idtbl[x][y]
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
                elif type(ide) is tuple:
                    f = 'orange'
                dungeon.create_rectangle(
                                        x*(tilesize),
                                        (y*(tilesize)),
                                        ((x+1)*(tilesize))-1,
                                        ((y+1)*(tilesize))-1,
                                        fill=f,
                                        outline=o,
                                        width=w
                                        )
                dungeon.pack()
        self.master.mainloop()
        
    def _format(self,size, sx,sy):
        """ Recieves a x and y position and creates the type needed to create it """
        try:
            width, height = size
        except:
            width = height = size
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
        checkVals = [(x,y) for x,y in self.notnull if self.cantouch[  x][  y  ] != 1]
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
        ''' Scans through the list and removes all walls '''
        checkVals = [(x,y) for x,y in self.notnull if self.Idtbl[ x ][ y ] == 1]
        for x,y in checkVals :
            self.Idtbl[x][y] = 0

    def make_start_pos(self):
            x,y = self.notnull[ self._Prng(len(self.notnull)) ]
            moveX , moveY = self.__findDir( self._Prng(4) )
            newX , newY = x + moveX , y + moveY
            try:
                if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0 and self.Idtbl[x][y] != 3:
                    self.start_room = Room(1, 1, newX, newY, self.notnull, self.Idtbl,self)
                    self.start_pos = (newX, newY)
                    self.Idtbl[newX][newY] = 5
                    #TODO dont forget to add a door after this 
                else:
                    self.make_start_pos()
            except IndexError:
                self.make_start_pos()
            
            
class Room:
    ''' A class that contains its own pair of blocks and monsters'''
    def __init__(self, size, how, sx,sy, notnull, idtbl, dungeon ,is_boss = False):
        self.dungeon = dungeon
        try:
            self.width,self.height = size
        except:
            self.width,self.height = size,size
        self.size = size
        if how == 0:
            self.blocks = [Tile(self, size, (sx + x , sy + y) ) for y in range(self.height) for x in range(self.width)]
        elif how == 1:
            self.blocks = [Tile(self , size, (sx - x , sy + y )) for y in range(self.height) for x in range(self.width)]
        elif how == 2:
            self.blocks = [Tile(self, size , (sx - x , sy - y )) for y in range(self.height) for x in range(self.width)]
        elif how == 3:
            self.blocks = [Tile(self, size, (sx + x , sy - y )) for y in range(self.height) for x in range(self.width)]
        self.blocks.sort()
        for tile in self.blocks:
            x,y = tile.position
            notnull.append((x,y))
            idtbl[x][y] = size
        if is_boss:
            self.monsters = BossMonster(self, 1)
        else:
            self.monsters = [Monster(self) for x in range(random.randint(0,1))]

    def room_draw(self):
        for tile in self.blocks:
            tile.tile_draw()

    def __repr__(self):
        return "Room: {},{}".format(self.width, self.height)

    def newDoor(self, tile, position):
        for square in self.blocks:
            if square is tile:
                tile.addDoor(position)      


class Tile:
    tile_size = 16
    def __init__(self, Room, _type, position):
        '''Recieves its room, the type of tile it is, and the X,Y coordinates as a tuple'''
        self.room = Room
        self.position = position
        self.doors = {"North":0,"South":0,"East":0, "West":0}
        self.x , self.y = self.position
        self.display = self.room.dungeon.game.display
        self.image = get_img("Tile",random.randint(2,73))
        self.isDoor = False

    def addDoor(self, positon):
        '''Recievs a Position North South East and West and changes the values of the door'''
        if position == 'N': self.doors["North"] = 1
        elif position == 'S': self.doors["South"] = 1
        elif position == 'E': self.doors["East"] = 1
        elif position == 'W': self.doors["West"] = 1
        self.isDoor = True

    
    @classmethod
    def set_tile_size(cls, size):
        ''' Recieves the size of the new tile and sets it to the defalts '''
        cls.tile_size = size


    def tile_draw(self):
        # TODO Import the pictures
        # TODO size = 360/resolution * Size of image
        if self.tile_size != 16:
            self.image = pygame.transform.scale(self.image,(self.tile_size, self.tile_size))
        self.display.blit(self.image, (self.x * self.tile_size, self.y * self.tile_size))


    def __lt__(self, other):
        return self.position < other.position
    
    def __eq__(self, other):
        return self.position == other.position


class Wall(pygame.sprite.Sprite):
    wall_size = 32
    def __init__(self, position, Dungeon):
        """
        Recieves an X and Y position and the dungeon instance
        """
        pygame.sprite.Sprite.__init__(self)
    
    def draw():
        pass


if __name__ == "__main__":
    try:
        pygame.init()
        d = Dungeon( resolution = (20,20), roomCount = 25, specialWeigth= 2)
        d.make()
        d._draw(tilesize = 32)
    except KeyboardInterrupt as e:
        print(d.seed)
