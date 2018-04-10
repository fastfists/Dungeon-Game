from classydungeon import *

class DungeonElement:
    ''' Abstract class that is for all elements of the dungeon'''
    def __init__(self,position, dungeon):
        self.image = None
        self.display = dungeon.game.display
        dungeon.elements.append(self)
        self.x, self.y = position
        self.size = dungeon.game.TILESIZE



        # debuging reasons
        font = pygame.font.SysFont(None, 20)
        self.text = font.render(f"{self.x},{self.y}", True, utils.BLACK)

    @property
    def position(self):
        return self.x, self.y

    def __repr__(self):
        return "{}: is located at {} , {}".format(self.__class__.__name__, self.x, self.y)

    def draw(self):
        '''
        blits the sprite onto the screen
        '''
        
        if not self.image:
            raise NameError("Set the image to draw as self.image")
        self.display.blit(self.image,(self.x * self.size, self.y * self.size))
        self.display.blit(self.text,(self.x * self.size, self.y * self.size))


class Room:
    ''' A class that contains its own pair of blocks and monsters'''
    def __init__(self, size, how, sx,sy, dungeon ,is_boss = False):
        self.dungeon = dungeon
        try:
            self.width,self.height = size
        except:
            self.width,self.height = size,size
        self.size = size
        if how == 0:
            self.blocks = [Tile((sx + x , sy + y), self) for y in range(self.height) for x in range(self.width)]
        elif how == 1:
            self.blocks = [Tile((sx - x , sy + y ), self) for y in range(self.height) for x in range(self.width)]
        elif how == 2:
            self.blocks = [Tile((sx - x , sy - y ), self) for y in range(self.height) for x in range(self.width)]
        elif how == 3:
            self.blocks = [Tile((sx + x , sy - y ), self) for y in range(self.height) for x in range(self.width)]
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


class Tile(DungeonElement):
    def __init__(self, position, Room):
        '''Recieves its room, the type of tile it is, and the X,Y coordinates as a tuple'''
        super().__init__(position, Room.dungeon)
        self.image = utils.get_img("Tile", 17)
        self.image = pygame.transform.scale(self.image,(self.tile_size, self.tile_size))
        self.room = Room
        self.type = self.room.size

    def __lt__(self, other):
        return self.position < other.position
    
    def __eq__(self, other):
        return self.position == other.position


class Wall(DungeonElement):

    def __init__(self, position, Dungeon, direction):
        """
        Recieves an X and Y position and the dungeon instance
        """
        super().__init__(position, Dungeon)

        self.image = utils.get_img("Tile", 5)
        
        if direction == (0, 1):
            self.image = pygame.transform.rotate(self.image, 180)
        elif direction == (1, 0):
            self.image = pygame.transform.rotate(self.image, 270)
        elif direction == (-1, 0):
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction == (0, -1):
            self.image = utils.get_img("Tile", 1)
        
        self.image = pygame.transform.scale(self.image,(self.size, self.size))        
            

class Door(DungeonElement):
    
    def __init__(self, x, y, dungeon, direction):
        super().__init__((x,y), dungeon)
        self.image = utils.get_img("Door",53)
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
        if direction[0] == 0: 
            # Up and down
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction[1] == 0:
            # side to side
            self.image = pygame.transform.rotate(self.image, 270)

