from classydungeon import *

class Room:
    test = "test"
    ''' A class that contains its own pair of blocks and monsters'''
    def __init__(self, size, how, sx,sy, dungeon ,is_boss = False):
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
        
        # Adds its information to the dungeon ID table
        for tile in self.blocks:
            # this does the "dirty work" for me instead of handling it in the dungeon
            x,y = tile.position
            self.dungeon.notnull.append((x,y))
            self.dungeon.Idtbl[x][y] = size

        
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
            tile.draw()
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
    def __init__(self, Room, position):
        '''Recieves its room, the type of tile it is, and the X,Y coordinates as a tuple'''
        self.position = position
        self.image = utils.get_img("Tile", 17)
        
        self.room = Room
        self.type = self.room.size
        self.display = self.room.dungeon.game.display
        self.image = pygame.transform.scale(self.image,(self.tile_size, self.tile_size))


    def tile_draw(self):
        self.display.blit(temp_image, (self.x * self.tile_size, self.y * self.tile_size))

    def __lt__(self, other):
        return self.position < other.position
    
    def __eq__(self, other):
        return self.position == other.position


class Wall():

    def __init__(self, position, Dungeon, direction):
        """
        Recieves an X and Y position and the dungeon instance
        """
        self.position = position
        self.x, self.y = position
        self.dungeon = Dungeon

        self.image = utils.get_img("Tile", 5)
        
        if direction == (0, 1):
            self.image = pygame.transform.rotate(self.image, 180)
        elif direction == (1, 0):
            self.image = pygame.transform.rotate(self.image, 270)
        elif direction == (-1, 0):
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction == (0, -1):
            self.image = self.image

            self.image = utils.get_img("Tile", 1)
        
        
        self.display = self.dungeon.game.display
            
         # Assume that it is a corner2 TODO change this 
        
    def draw(self):
        temp_image = pygame.transform.scale(self.image,(self.wall_size, self.wall_size))
        self.display.blit(temp_image, (self.x * self.wall_size, self.y * self.wall_size))


class Door():
    
    def __init__(self, x, y, dungeon, direction):
        pygame.sprite.Sprite.__init__(self)
        self.position = self.x, self.y = x,y
        self.dungeon = dungeon
        self.size = Tile.tile_size
        self.display = self.dungeon.game.display
        self.image = utils.get_img("Door",53)
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
        if direction[0] == 0: 
            # Up and down
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction[1] == 0:
            # side to side
            self.image = pygame.transform.rotate(self.image, 270)

    def draw(self):
        self.display.blit(self.image,(self.x * self.size, self.y * self.size))


class DungeonElement():
    ''' Abstract class that is for all elements of the dungeon'''
    def __init__(self,position, dungeon):
        self.image = None
        self.display = dungeon.game.display
        self.position = position
        self.size = dungeon.game.TILESIZE

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def __repr__(self):
        return "{}: at {} , {}".format(self.__class__.__name__, self.x, self.y)

    def draw():
        if not self.image:
            raise NameError("Set the image to draw as self.image")
        self.display.blit(self.image,(self.x * self.size, self.y * self.size))
