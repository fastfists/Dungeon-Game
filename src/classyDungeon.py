''' Contains Dungeon object and Room objects '''
import random
import utils
import pygame
import characters


class Dungeon:
    notnull = []
    allrooms = []
    currenType = -1
    '''
    __init__ method:
        - Resolution as a tuple (width,height)
        - Roomcount as an int
    '''
    def __init__(self ,resolution: tuple, roomCount, game, specialWeigth = 2 , seed = random.randint(0,879190747)):
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
        self.doors = []
        self.start_pos = (-1,-1)

    def _Prng(self,limit, wantBool = False):
        self.prngNum = (self.prngNum * 154687469+879190747) % 67280421310721
        if wantBool: return self.prngNum % limit == 0
        else: pass
        return self.prngNum % limit

    def __repr__(self):
        return f"Dungeon: {self.RESOLUTION} , {len(self.allrooms)}" 

    def make(self):
        works = False
        while not works:
            x,y = self._Prng(len(self.Idtbl)), self._Prng(len(self.Idtbl))
            if self._format(3,x,y):
                self.allrooms.append(Room(3, self.currenType,x,y,self.notnull, self.Idtbl, self,is_boss=True))
                self.update(3, self.currenType, x, y)
                self.addWalls()
                works = True
        while len(self.allrooms) != self.roomCount:
            self.works = False
            x,y = self.walls[ self._Prng(len(self.walls) - 1)].position # finds a random wall and gets the x and y
            moveX , moveY = self.__findDir( self._Prng(4) )
            newX , newY = x + moveX , y + moveY
            try:
                if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0:
                    if self._Prng(self.weight,wantBool=True):
                        size = (4,2)
                        self.weight *= 8
                    else:
                        if self._Prng(2,wantBool=True): # 50/50 chance
                            size = 4
                        else: size = 2
                    if self._format(size, newX,newY):
                        self.allrooms.append(Room(size, self.currenType,newX, newY , self.notnull, self.Idtbl,self))
                        newX , newY = self.__startVal(self.allrooms[ len(self.allrooms) - 1 ])
                        self.update(size, self.currenType,newX, newY)
                        self.addWalls()
                        self.Idtbl[x][y] = -1
                        self.doors.append(Door(x, y, self, (moveX,moveY)))
            except IndexError: pass
        self.make_start_room()
        self.addWalls(corners=True)

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

    def addWalls(self, corners=False):
        dir_index = 8
        if not corners:
            dir_index = 4
        checkVals = [(x,y) for x,y in self.notnull if self.cantouch[x][y] != 1 and self.Idtbl[x][y] != 1 and self.Idtbl[x][y] != -1]
        if checkVals != []:
            for tup in checkVals:
                x,y = tup
                for direction in range(dir_index):
                    nx,ny = self.__findDir(direction)
                    neighborX, neighborY = nx+x, ny+y
                    try:
                        if self.Idtbl[neighborX][neighborY] == 0 and neighborX >= 0 and neighborY >= 0:
                            self.Idtbl[neighborX][neighborY] = 1
                            self.walls.append(Wall((neighborX,neighborY),self))
                            self.notnull.append(neighborX, neighborY)
                    except:
                        pass

    def make_start_room(self):
            x,y = self.walls[ self._Prng(len(self.walls)) ].position
            moveX , moveY = self.__findDir( self._Prng(4) )
            newX , newY = x + moveX , y + moveY
            try:
                if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0 and self.Idtbl[x][y] != 3:
                    self.start_pos = (newX, newY)
                    self.start_room = Room(1, 1, newX, newY, self.notnull, self.Idtbl,self)
                    self.Idtbl[newX][newY] = 5
                    self.Idtbl[x][y] = -1
                    self.doors.append(Door(x, y, self, (moveX,moveY)))
                else:
                    self.make_start_room()
            except IndexError:
                self.make_start_room()
            
            
class Room:
    test = "test"
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
        if (sx,sy) != self.dungeon.start_pos:
            if is_boss:
                self.monsters = [characters.BossMonster(self, 1)]
            else:
                self.monsters = [characters.Monster(self) for x in range(random.randint(1,2))]
        else:
            self.monsters = None

    def activate(self):
        if not self.monsters == None:
            for monster in self.monsters:
                monster.patrol()

    def room_draw(self):
        for tile in self.blocks:
            tile.tile_draw()
        if not self.monsters == None:
            for monster in self.monsters:
                monster.show()

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
        self.x , self.y = self.position
        self.type = self.room.size
        self.display = self.room.dungeon.game.display
        self.hasDoor = False

        if self.type != 1: 
            self.image = utils.get_img("Tile",random.randint(3,70))
        elif type(self.type) is tuple:
            self.image = utils.get_img("Tile", 71)
        else: 
            self.image = utils.get_img("Tile",random.randint(71,73))

    def tile_draw(self):
        temp_image = pygame.transform.scale(self.image,(self.tile_size, self.tile_size))
        self.display.blit(temp_image, (self.x * self.tile_size, self.y * self.tile_size))

    def __lt__(self, other):
        return self.position < other.position
    
    def __eq__(self, other):
        return self.position == other.position


class Wall(pygame.sprite.Sprite):
    #TODO hey im over here !!!! give me stuff!!!
    wall_size = 16
    def __init__(self, position, Dungeon):
        """
        Recieves an X and Y position and the dungeon instance
        """
        self.position = position
        self.x, self.y = position
        self.Dungeon = Dungeon
        pygame.sprite.Sprite.__init__(self)
    
    def draw_wall(self):
        pass

    @classmethod
    def set_wall_size(cls,size):
        cls.wall_size = size

    def draw(self):
        pass

class Door:
    
    def __init__(self, x, y, dungeon, direction):
        self.position = self.x, self.y = x,y
        self.dungeon = dungeon
        direction = 'Vertical'
        direction = 'Horizantal'

    def draw_Door(self):
        pass


