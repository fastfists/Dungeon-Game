from classydungeon import *
import random
import pygame



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
            self.blocks = [Tile((sx - x , sy + y), self) for y in range(self.height) for x in range(self.width)]
        elif how == 2:
            self.blocks = [Tile((sx - x , sy - y), self) for y in range(self.height) for x in range(self.width)]
        elif how == 3:
            self.blocks = [Tile((sx + x , sy - y), self) for y in range(self.height) for x in range(self.width)]
        self.blocks.sort()
        
        # Adds its information to the dungeon ID table
        for tile in self.blocks:
            # this does the "dirty work" for me instead of handling it in the dungeon
            x,y = tile.position
            self.dungeon.notnull.append((x,y))
            self.dungeon.Idtbl[x][y] = size

        
        if (sx,sy) != self.dungeon.start_pos:
            if is_boss:
                pass
                #self.monsters = [characters.BossMonster(self, 1)]
                self.monsters = None
            else:
                self.monsters = [character.Monster(self) for x in range(random.randint(1,2))]
        else:
            self.monsters = None

    def activate(self):
        if not self.monsters == None:
            for monster in self.monsters:
                monster.patrol()

    def room_draw(self):
        for tile in self.blocks:
            tile.draw()
        '''if not self.monsters == None:
            for monster in self.monsters:
                monster.show()'''

    def __repr__(self):
        return "Room: {},{}".format(self.width, self.height)

class DungeonElement:
    ''' Abstract class that is for all elements of the dungeon'''
    def __init__(self,position, dungeon):
        #assert self.image != NotImplemented, "Dont forget to apply an image"
        self.display = dungeon.game.display
        self.x, self.y = position
        dungeon.elements.add(self)
        self.size = dungeon.TILESIZE
        self.dungeon = dungeon
        # debuging reasons
        font = pygame.font.SysFont(None, 20)
        self.text = font.render(f"{self.x},{self.y}", True, utils.BLACK)

    @classmethod
    def from_room(self, room:Room):
        self.__init__(self, random.choice(room.blocks).position, room.dungeon)

    def __hash__(self):
        # TODO Change this hashing for Sprite elements
        return hash((self.x, self.y))

    @property
    def position(self):
        return self.x, self.y

    def __repr__(self):
        return f"{self.__class__.__name__}: located at {self.x} , {self.y}"

    def draw(self, size=None):
        '''
        blits the sprite onto the screen
        '''
        if isinstance(self,pygame.sprite.Sprite):
            print(self.x * self.dungeon.TILESIZE, self.dungeon.WIDTH*self.dungeon.TILESIZE )
        if size:
            pass
            temp_img = pygame.transform.scale(self.image, (size, size))
            temp_img.set_alpha(100)
            self.display.blit(temp_img,(self.x * size, self.y * size))
        else:
            self.display.blit(self.text,(self.x * self.dungeon.TILESIZE, self.y * self.dungeon.TILESIZE))
            self.display.blit(self.image,(self.x * self.dungeon.TILESIZE, self.y * self.dungeon.TILESIZE))

import character

class Tile(DungeonElement):
    def __init__(self, position, Room):
        '''Recieves its room, the type of tile it is, and the X,Y coordinates as a tuple'''
        self.image = utils.get_img("Tile", 17)
        super().__init__(position, Room.dungeon)
        self.image = pygame.transform.scale(self.image,(self.size, self.size))
        self.room = Room
        self.type = self.room.size

    def __lt__(self, other):
        return self.position < other.position
    


class Wall(DungeonElement):
    image = utils.get_img("Tile", 5)
    def __init__(self, position, Dungeon, direction):
        """
        Recieves an X and Y position and the dungeon instance
        """
        super().__init__(position, Dungeon)


        
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
        self.image = utils.get_img("Door",59)    
        super().__init__((x,y), dungeon)
        self.image = pygame.transform.scale(self.image, (self.size,self.size))

        """if direction[0] == 0: 
            # Up and down
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction[1] == 0:
            # side to side
            self.image = pygame.transform.rotate(self.image, 270)"""

