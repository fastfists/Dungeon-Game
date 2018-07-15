''' Contains Dungeon object and Room objects '''
import dungeon_utils
import random
import utils
import pygame
import character
import numpy as np
import json
from collections import namedtuple

class Dungeon:
    """
    The dungeon uses a method of Procedual generation that I created without any outside info on the topic
    It operates using Room Identies and "Touchable blocks" The Identity list is as follows:

      5 -     Refers to the Starting room for the player, Is unique and created at the end of the function
      4 -     Refers to a 4X4 room this is chosen randomly between the 2X2 and 4X2
      3 -     Refers to the Boss room, Is unique and created at the begining of the algorithim
      2 -     Refers to a 3 X 3 room this is chosen randomly between the 4X4 and 4X2
      1 -     Refers to a Wall
      (4,2) - Refers to a 4*2 room this is chosen randomly between the 4X4 and 2X2
      0 -     Any null block
      -1 -    Door blocks
      I would have set up constants, but forgot to and now its a bit to late / I am lazy and want to move on the the game
    """

    '''
    __init__ method:
        - Resolution as a tuple (width,height)
        - Roomcount as an int
    '''

    def __init__(self, resolution, room_count, game, specialWeigth=2, seed=random.randint(0, 879190747)):
        self.game = game
        self.display = game.display
        self.prngNum = seed
        self.seed = self.prngNum
        self.RESOLUTION = resolution
        self.WIDTH, self.HEIGHT = self.RESOLUTION
        self.room_count = room_count
        self.cantouch = [[0 for _ in range(self.HEIGHT)] for _ in range(self.WIDTH)]
        self.Idtbl = [[0 for _ in range(self.HEIGHT)] for _ in range(self.WIDTH)]
        self.weight = specialWeigth
        self.start_pos = (-1, -1)  # set it to an unreachable point to begin with to make the room class happy
        self.notnull = []
        self.allrooms = []
        self.currenType = -1
        self.walls = []
        self.border = []
        self.doors = []
        self.elements = pygame.sprite.Group()
        self.TILESIZE = game.TILESIZE
        self.background = pygame.surface.Surface((self.WIDTH*self.TILESIZE, self.HEIGHT*self.TILESIZE))

    def __repr__(self):
        return f"Dungeon: {self.RESOLUTION} , {len(self.allrooms)}"

    @classmethod
    def from_json(cls, file_name, game, **extras):
        data = json.load(open(file_name))
        data["game"] = game
        return cls(**data)

    def _Prng(self, limit, wantBool=False):
        """ 
            Randomizer
            :param limit: The highest value (2 returns 1 or 0)
            :returns: int
        """
        self.prngNum = (self.prngNum * 154687469 + 879190747) % 67280421310721
        if wantBool: return self.prngNum % limit == 0
        return self.prngNum % limit

    def make(self):
        self.add_border()
        works = False
        while not works:
            x, y = self._Prng(len(self.Idtbl)), self._Prng(len(self.Idtbl))
            if self._format(6, x, y):
                self.allrooms.append(dungeon_utils.Room(6, self.currenType, x, y, self, is_boss=True))
                x, y = self.__startVal(self.allrooms[len(self.allrooms) - 1])
                self.update(6, self.currenType, x, y)
                self.addwalls()
                works = True
        while len(self.allrooms) != self.room_count:
            self.works = False
            x, y = self.walls[self._Prng(len(self.walls))].position  # finds a random wall and gets the x and y
            moveX, moveY = self._findDir(self._Prng(4))
            newX, newY = x + moveX, y + moveY
            try:
                if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0 and self.door_fits((x,y), (moveX, moveY)):
                    if self._Prng(self.weight, wantBool=True):
                        size = (8, 4)
                        self.weight *= 8
                    else:
                        if self._Prng(2, wantBool=True):  # 50/50 chance
                            size = 8
                        else:
                            size = 4
                    if self._format(size, newX, newY):
                        self.allrooms.append(dungeon_utils.Room(size, self.currenType, newX, newY, self))
                        newX, newY = self.__startVal(self.allrooms[len(self.allrooms) - 1])
                        self.update(size, self.currenType, newX, newY)
                        self.addwalls()
                        self.Idtbl[x][y] = -1
                        self.doors.append(dungeon_utils.Door(x, y, self, (moveX, moveY)))
                        self.remove_wall_at(x,y)
            except IndexError:
                pass
        self.make_start_room()
        self.update_all()
        self.addwalls(corners=True)
        self._finalize()

    def find_block_at(self, pos:tuple) -> dungeon_utils.Background:
        """ Recieves a x and y postion as a tuple and returns a Background object"""
        for room in self.allrooms:
            for block in room.blocks:
                if block.position == pos:
                    return block
            

    def find_room_at(self, pos:tuple):
        try:
            return self.find_block_at(pos).room
        except AttributeError as e:
            return None

    def remove_wall_at(self, x, y):
        for i, wall in enumerate(self.walls):
            if wall.position == (x,y):
                del self.walls[i]


    def door_fits(self, positon, move_vector)->bool:
        ### Find closet room/block ###
        def check(old_direc, new_direc):
            old, new = np.array(old_direc), np.array(new_direc)
            result = (old + new).tolist()
            return result == [0,0]

        x, y =positon
        for move_x, move_y in map(self._findDir, range(4)):
            if (move_x, move_y) == move_vector:
                continue
            block = self.Idtbl[x+move_x][y+move_y]
            print(block)
            if block != 0 and block != 1 and block != -1:
                ## We have reched a tile
                direction = move_x, move_y
                break
        print(self.allrooms)
        print("--------------------")
        return check(move_vector, direction)

    @staticmethod
    def __startVal(room):
        return room.blocks[0].position

    def _format(self, size, sx, sy):
        """ Recieves a x and y position and creates the type needed to create it """
        try:
            width, height = size
        except:
            width = height = size
        for typ in range(4):
            works = True
            for y in range(height):
                for x in range(width):
                    if typ == 0:
                        newX, newY = sx + x, sy + y
                    elif typ == 1:
                        newX, newY = sx - x, sy + y
                    elif typ == 2:
                        newX, newY = sx - x, sy - y
                    elif typ == 3:
                        newX, newY = sx + x, sy - y
                    else:
                        return False
                    try:
                        if self.Idtbl[newX][newY] != 0:
                            works = False
                            break
                    except:
                        works = False
                        break
                    if (newX, newY) in self.notnull or newX < 0 or newY < 0:
                        works = False
                        break  # breaks from X loop
                if not works:
                    break
            if works:
                self.currenType = typ
                return works
        return False  # retdoorurns False because none of the types work

    def update(self, size, how, startX, startY):
        for y in range(startY + 2):
            for x in range(startX + 2):
                _pass = True
                for d in range(4):
                    dirX, dirY = self._findDir(d)
                    neighborX, neighborY = dirX + x, dirY + y
                    try:
                        self.Idtbl[neighborX][neighborY]
                    except IndexError:
                        _pass = False
                        break
                    if (neighborX, neighborY) not in self.notnull:
                        _pass = False
                        break
                if _pass == True and self.cantouch[x][y] == 0:
                    try:
                        self.cantouch[x][y] = 1
                    except ValueError:
                        pass

    def update_all(self):
        check_vals = [(x, y) for x, y in self.notnull if self.Idtbl[x][y] != 1]
        for tup in check_vals:
            x, y = tup
            _pass = True
            for d in range(8):
                dirX, dirY = self._findDir(d)
                neighborX, neighborY = dirX + x, dirY + y
                try:
                    self.Idtbl[neighborX][neighborY]
                except IndexError:
                    _pass = False
                    break
                if (neighborX, neighborY) not in self.notnull:
                    _pass = False
                    break
            if _pass == True and self.cantouch[x][y] == 0:
                try:
                    self.cantouch[x ][y] = 1
                except IndexError:
                    pass
            else:
                self.cantouch[x][y] = 0
                self.notnull.append((x, y))

    @staticmethod
    def _findDir(dir_index):
        ''' A more conventional method to find the x and y positions '''
        if dir_index == 0:
            return (1, 0)
        if dir_index == 1:
            return (-1, 0)
        if dir_index == 2:
            return (0, 1)
        if dir_index == 3:
            return (0, -1)
        if dir_index == 4:
            return (-1, -1)
        if dir_index == 5:
            return (1, -1)
        if dir_index == 6:
            return (-1, 1)
        if dir_index == 7:
            return (1, 1)

    def addwalls(self, corners=False):
        if not corners:
            dir_index = 4
            checkVals = [(x, y) for x, y in self.notnull if
                         self.cantouch[x][y] != 1 and self.Idtbl[x][y] != 1 and self.Idtbl[x][y] != -1]
        else:
            dir_index = 8
            checkVals = [(x, y) for x, y in self.notnull if self.Idtbl[x][y] != 1]
        if checkVals != []:
            for tup in checkVals:
                x, y = tup
                for direction in range(dir_index):
                    nx, ny = self._findDir(direction)
                    neighborX, neighborY = nx + x, ny + y
                    try:
                        if self.Idtbl[neighborX][neighborY] == 0 and neighborX >= 0 and neighborY >= 0:
                            self.Idtbl[neighborX][neighborY] = 1
                            temp_wall = dungeon_utils.Wall((neighborX, neighborY), self, (nx, ny))
                            self.walls.append(temp_wall)
                            self.notnull.append((neighborX, neighborY))
                    except IndexError:
                        pass

    def make_start_room(self):
        x, y = self.walls[self._Prng(len(self.walls))].position
        moveX, moveY = self._findDir(self._Prng(4))
        newX, newY = x + moveX, y + moveY
        try:
            if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0 and self.Idtbl[x][y] != 3 and newX > 0 and newY > 0:
                self.start_pos = (newX, newY)
                self.start_room = dungeon_utils.Room(1, 1, newX, newY, self)
                self.Idtbl[newX][newY] = 5
                self.Idtbl[x][y] = -1
                self.doors.append(dungeon_utils.Door(x, y, self, (moveX, moveY)))
                self.remove_wall_at(x, y)
            else:
                self.make_start_room()
        except IndexError:
            self.make_start_room()


    def add_border(self):
        for i in range(self.WIDTH):
            self.border.append(dungeon_utils.Wall((i, 0), self, (0,0)))
            self.Idtbl[i][0] = 1
            self.border.append(dungeon_utils.Wall((i, self.HEIGHT - 1), self, (0,0)))
            self.Idtbl[i][-1] = 1
        for i in range(self.HEIGHT):
            self.border.append(dungeon_utils.Wall((0, i), self, (1, 0)))
            self.Idtbl[-1][i] = 1
            self.border.append(dungeon_utils.Wall((self.WIDTH - 1, i), self, (-1, 0)))
            self.Idtbl[0][i] = 1

    @property
    def monsters(self):
        return [element for element in self.elements if isinstance(element, character.Monster)]

    def _finalize(self):
        """ This method sets all variables
        for the main game loop
        """
        self.player = character.Player(self)
        self.make_order()
        [door.find_rooms() for door in self.doors]
        self.background = self.make_background(self.background)

    def make_background(self, background:pygame.surface.Surface):
        class target:
            def __init__(self, x, y):
                self.x = x
                self.y = y            
        draw_args = dict()
        [wall.draw(display=background, target=target(0,0), background=True) for wall in self.walls]
        [wall.draw(display=background, target=target(0,0), background=True) for wall in self.border]
        
        for room in self.allrooms+ [self.start_room]:
            print(room)
            [tile.draw(display=background, target=target(0,0), background=True) for tile in room.blocks]
        background.set_colorkey(utils.BLACK)
        return background

    def make_order(self):
        [self.elements.add(room.all_elements()) for room in self.allrooms]
        [self.elements.add(wall) for wall in self.border + self.walls]
        self.elements.add(self.start_room.all_elements())
        [self.elements.add(door) for door in self.doors]
        self.elements.add(self.player)
        print("Im useful still")

    def _draw(self, tile_size=None):
        """The draw and update method for the dungeon
        """
        """        if tile_size:
            background_img = pygame.transform.scale(self.background, (tile_size, tile_size))
            background_img.set_alpha(100)
        else:
            background_img = self.background"""
        self.focus = self.player
        x = -self.focus.x + self.game.GRIDWIDTH // 2
        y = -self.focus.y + self.game.GRIDHEIGHT// 2
        self.display.blit(self.background, (x*self.TILESIZE, y*self.TILESIZE))
        
        for room in self.allrooms:
            [monster.draw() for monster in room.monsters]
        [door.draw() for door in self.doors]
        self.player.draw()
        self.player.update()
