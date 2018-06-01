import random
import pygame
import utils
import numpy as np

class DungeonElement:
    """ Abstract class that is for all elements of the dungeon """
    image = None

    def __init__(self, position, dungeon):
        assert self.image, "Dont forget to apply an image"
        self.display = dungeon.game.display
        self.x, self.y = position
        self.size = dungeon.TILESIZE
        self.dungeon = dungeon
        self.rect = self.image.get_rect()
        # debuging reasons

    @property
    def true_pos(self):
        pos = np.array(self.position)
        dungeon_scale = np.array([self.dungeon.TILESIZE, self.dungeon.TILESIZE])
        return tuple(pos * dungeon_scale)

    def __lt__(self, other):
        meInstance = isinstance(self, character.Sprite)
        otherInstance = isinstance(other, character.Sprite)
        if not meInstance and otherInstance:
            return True
        elif not meInstance and not otherInstance:
            meInstance = isinstance(self, Door)
            otherInstance = isinstance(other, Door)
            if not meInstance and otherInstance:
                return True

    def __hash__(self):
        # TODO Change this hashing for Sprite elements
        return hash((self.x, self.y))

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, new_position:tuple):
        self.x, self.y = new_position

    @property
    def graph_position(self):
        return round(self.x), round(self.y)

    def __repr__(self):
        return f"{self.__class__.__name__}: located at {self.x} , {self.y}"

    def kill(self):
        super().kill() # for sprites
        self.dungeon.elements.remove(self)

    def transform(self, x, y):
        self.rect.x, self.rect.y = ((x+self.x) * self.dungeon.TILESIZE, (y + self.y) * self.dungeon.TILESIZE)

    def scale(self, size:tuple):
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

    def draw(self, size=None, flip=False):
        """
        Blits the element onto the screen
        """
        if size:

            temp_img = pygame.transform.scale(self.image, (size, size))
            temp_img.set_alpha(100)
            self.display.blit(temp_img, (self.x * size, self.y * size))
        else:
            # self.display.blit(self.text,(self.x * self.dungeon.TILESIZE, self.y * self.dungeon.TILESIZE))
            self.scale((self.size, self.size))
            temp_img = pygame.transform.flip(self.image, flip, False)
            # temp_img.set_alpha(100)
            target = self.dungeon.focus
            x = -target.x + self.dungeon.game.GRIDWIDTH // 2
            y = -target.y + self.dungeon.game.GRIDHEIGHT // 2
            self.transform(x, y)
            pygame.draw.rect(self.display, utils.RED, self.rect)
            self.display.blit(temp_img, self.rect)

import character


class Room:
    ''' A class that contains its own pair of blocks and monsters'''

    def __init__(self, size, how, sx, sy, dungeon, is_boss=False):
        self.dungeon = dungeon
        try:
            self.width, self.height = size
        except:
            self.width, self.height = size, size
        self.size = size
        if how == 0:
            self.blocks = [Tile((sx + x, sy + y), self) for y in range(self.height) for x in range(self.width)]
        elif how == 1:
            self.blocks = [Tile((sx - x, sy + y), self) for y in range(self.height) for x in range(self.width)]
        elif how == 2:
            self.blocks = [Tile((sx - x, sy - y), self) for y in range(self.height) for x in range(self.width)]
        elif how == 3:
            self.blocks = [Tile((sx + x, sy - y), self) for y in range(self.height) for x in range(self.width)]
        self.blocks.sort()
        # Adds its information to the dungeon ID table
        for tile in self.blocks:
            # this does the "dirty work" for me instead of handling it in the dungeon
            x, y = tile.position
            self.dungeon.notnull.append((x, y))
            self.dungeon.Idtbl[x][y] = size

        if (sx, sy) != self.dungeon.start_pos:
            if is_boss:
                # self.monsters = [characters.BossMonster(self, 1)]
                self.monsters = [character.BossSkeleton(self)]
            else:
                self.monsters = [character.Skeleton(self) for x in range(random.randint(3, 5))]
        else:
            self.monsters = []

    def activate(self):
        if not self.monsters == None:
            for monster in self.monsters:
                monster.update()

    def draw(self, *args, **kwargs):
        [tile.draw(*args, **kwargs) for tile in self.blocks]
        [monster.draw(*args, **kwargs) for monster in self.monsters]

    def __repr__(self):
        return "Room: {},{}".format(self.width, self.height)


class Tile(DungeonElement, pygame.sprite.Sprite):
    def __init__(self, position, Room):
        """Recieves its room, the type of tile it is, and the X,Y coordinates as a tuple"""
        self.image = utils.get_img("Tile", 17)
        super().__init__(position, Room.dungeon)
        pygame.sprite.Sprite.__init__(self)
        self.scale((self.size, self.size))
        self.room = Room
        self.type = self.room.size

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y == other.y:
            if self.x < other.x:
                return True
        return False

    def __gt__(self, other):
        if self.y > other.y:
            return True
        elif self.y == other.y:
            if self.x > other.x:
                return True
        return False


class Wall(DungeonElement, pygame.sprite.Sprite):
    image = utils.get_img("Tile", 5)

    def __init__(self, position, Dungeon, direction):
        """
        Recieves an X and Y position and the dungeon instance
        """
        super().__init__(position, Dungeon)
        pygame.sprite.Sprite.__init__(self)
        if direction == (0, 1):
            self.image = pygame.transform.rotate(self.image, 180)
        elif direction == (1, 0):
            self.image = pygame.transform.rotate(self.image, 270)
        elif direction == (-1, 0):
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction == (0, -1):
            self.image = utils.get_img("Tile", 1)

        self.scale((self.size, self.size))


class Door(DungeonElement, pygame.sprite.Sprite):
    def __init__(self, x, y, dungeon, direction):
        self.image = utils.get_img("Door", 59)
        super().__init__((x, y), dungeon)
        self.scale((self.size, self.size))
        pygame.sprite.Sprite.__init__(self)
        """if direction[0] == 0:
            # Up and down
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction[1] == 0:
            # side to side
            self.image = pygame.transform.rotate(self.image, 270)"""

