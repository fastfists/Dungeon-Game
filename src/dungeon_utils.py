import random

import numpy as np
import pygame

from . import utils

class DungeonElement(pygame.sprite.Sprite):
    """ Abstract class that is for all elements of the dungeon """
    image = None

    def __init__(self, position, dungeon):
        assert self.image, "Dont forget to apply an image"
        super().__init__()
        self.display = dungeon.game.display
        self.x, self.y = position
        self.size = dungeon.TILESIZE
        self.dungeon = dungeon
        self.dungeon.elements.add(self)
        self.rect = self.image.get_rect()
        # debuging reasons

    @property
    def true_pos(self):
        pos = np.array(self.position)
        dungeon_scale = np.array([self.dungeon.TILESIZE, self.dungeon.TILESIZE])
        return tuple(pos * dungeon_scale)

    def __hash__(self):
        # TODO Change this hashing for Sprite elements
        return hash((self.x, self.y))

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, new_size):
        self._size = new_size
        if isinstance(self, character.Sprite):
            self.health.width = self.width

    @property
    def width(self):
        return self.size // 2

    @property
    def height(self):
        return self.size

    @width.setter
    def width(self, new_width):
        self.size = new_width * 2  # multiply by 2 to adjust for the getter method

    @height.setter
    def height(self, new_height):
        self.size = new_height

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, new_position: tuple):
        self.x, self.y = new_position

    @property
    def graph_position(self):
        return round(self.x), round(self.y)

    def __repr__(self):
        return f"{self.__class__.__name__}: located at {self.x} , {self.y}"

    def transform(self, x, y):
        self.rect.x, self.rect.y = ((x + self.x) * self.dungeon.TILESIZE, (y + self.y) * self.dungeon.TILESIZE)

    def scale(self, size: tuple):
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

    def kill(self):
        super().kill()

    def draw(self, size=None, flip=False, display=None, target=None, background=False):
        """
        Blits the element onto the screen
        """
        if display:
            self.display = display

        if not target:
            target = self.dungeon.focus

        if size:
            temp_img = pygame.transform.scale(self.image, (size, size))
            temp_img.set_alpha(100)
            self.display.blit(temp_img, (self.x * size, self.y * size))
        else:
            # self.display.blit(self.text,(self.x * self.dungeon.TILESIZE, self.y * self.dungeon.TILESIZE))
            self.scale((self.width, self.height))
            temp_img = pygame.transform.flip(self.image, flip, False)
            # temp_img.set_alpha(100)
            if background:
                target.x = self.dungeon.game.GRIDWIDTH // 2 - target.x
                target.y = self.dungeon.game.GRIDHEIGHT // 2 - target.y
            x = -target.x + self.dungeon.game.GRIDWIDTH // 2
            y = -target.y + self.dungeon.game.GRIDHEIGHT // 2
            self.transform(x, y)
            # pygame.draw.rect(self.display, utils.RED, self.rect)
            self.display.blit(temp_img, self.rect)

from . import artifacts, character

class Room:
    """ A class that contains its own pair of blocks and monsters"""

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
            if type(size) is tuple:
                size = sum(size)
            self.dungeon.notnull.add((x,y))
            self.dungeon.Idtbl[x][y] = size
        self.doors = []
        if (sx, sy) != self.dungeon.start_pos:
            if is_boss:
                self.monsters = [character.BossSkeleton(self)]
            else:
                self.monsters = [character.Skeleton(self) for x in range(random.randint(3, 5))]
            self.chest = artifacts.Chest.chest_with_health_potion(self.blocks[0].position, self.dungeon)
        else:
            # it is the start room
            self.monsters = []
        self.is_cleared = self.check_if_cleared()

    def all_elements(self):
        for element in self.blocks + self.monsters:
            yield element

    def add_door(self, door):
        self.doors.append(door)

    def check_if_cleared(self) -> bool:
        self.is_cleared = all([monster.dead for monster in self.monsters])

    @property
    def active(self):
        return self.dungeon.focus.graph_position in self.block_positions

    @property
    def block_positions(self):
        return [block.position for block in self.blocks]

    @utils.do_once
    def open_doors(self):
        [door.open() for door in self.doors]
    
    @utils.do_once
    def close_doors(self):
        [door.close() for door in self.doors]

    def update(self):
        active = self.active
        if self.is_cleared:
            self.chest.update()
            self.open_doors()
        if not self.monsters == None:
            for monster in self.monsters:
                monster.update(active)
        if active:
            self.close_doors()

    def draw(self, *args, **kwargs):
        [monster.draw(*args, **kwargs) for monster in self.monsters]
        if self.is_cleared:
            self.chest.draw()

    def __repr__(self):
        return "Room: {},{}".format(self.width, self.height)


class Background(DungeonElement):
    """
    Just a class to modify all background elements
    """

    @property
    def width(self):
        return self.size

    @property
    def height(self):
        return self.size


class Tile(Background):
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


class Wall(Background):
    image = utils.get_img("Tile", 5)

    def __init__(self, position, Dungeon, direction):
        """
        Recieves an X and Y position and the dungeon instance
        """
        super().__init__(position, Dungeon)
        pygame.sprite.Sprite.__init__(self)
        if direction == (1, 0) or direction == (-1, 0):
            self.image = utils.get_img("Tile", 1)
        elif direction[0] and direction[1]:

            self.image = utils.get_img("Tile", 1)
            if direction == (-1, 1) or direction == (1, 1):
                self.image = utils.get_img("Tile", 5)

        self.scale((self.size, self.size))

class Door(Background):

    def __init__(self, x, y, dungeon, direction):
        self._state = "Closed"
        self.image = utils.get_img("Tile", 18)
        super().__init__((x, y), dungeon)
        self.scale((self.size, self.size))
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        if direction[1] == 0:
            # side to side
            self.image = pygame.transform.rotate(self.image, 270)
        self.rooms = []

    def find_rooms(self):
        from .classydungeon import Dungeon
        for x_move, y_move in map(Dungeon._findDir, range(4)):
            block = self.x + x_move, self.y + y_move
            room = self.dungeon.find_room_at(block)
            if room:
                room.add_door(self)

    def open(self):
        self.image = utils.get_img("Tile", 17)
        self.state = "Open"

    def close(self):
        self.image = utils.get_img("Tile", 18)
        if self.direction[1] == 0:
            # side to side
            self.image = pygame.transform.rotate(self.image, 270)
        self.state = "Closed"
