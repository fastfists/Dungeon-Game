''' Contains Dungeon object and Room objects '''
import dungeon_utils
import random
import utils
import pygame
import character
import json


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
        self.elements = []
        self.TILESIZE = game.TILESIZE



    def __repr__(self):
        return f"Dungeon: {self.RESOLUTION} , {len(self.allrooms)}"

    @classmethod
    def from_json(cls, file_name, game, **extras):
        data = json.load(open(file_name))
        data["game"] = game
        return cls(**data)

    def _Prng(self, limit, wantBool=False):
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
            moveX, moveY = self.__findDir(self._Prng(4))
            newX, newY = x + moveX, y + moveY
            try:
                if self.Idtbl[newX][newY] == 0 and self.cantouch[x][y] == 0:
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

    def remove_wall_at(self, x, y):
        for i, wall in enumerate(self.walls):
            if wall.position == (x,y):
                del self.walls[i]


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
                    dirX, dirY = self.__findDir(d)
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
                dirX, dirY = self.__findDir(d)
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
    def __findDir(dir_index):
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
                    nx, ny = self.__findDir(direction)
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
        moveX, moveY = self.__findDir(self._Prng(4))
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

    def _finalize(self):
        """ This method sets all variables
        for the main game loop
        """
        self.player = character.Player(self)
        self.elements.append(self.player)
        self.focus = self.player

    def add_border(self):
        for i in range(self.WIDTH):
            self.border.append(dungeon_utils.Wall((i, 0), self, 0))
            self.Idtbl[i][0] = 1
            self.border.append(dungeon_utils.Wall((i, self.HEIGHT - 1), self, 3))
            self.Idtbl[i][-1] = 1
        for i in range(self.HEIGHT):
            self.border.append(dungeon_utils.Wall((0, i), self, (1, 0)))
            self.Idtbl[-1][i] = 1
            self.border.append(dungeon_utils.Wall((self.WIDTH - 1, i), self, (-1, 0)))
            self.Idtbl[0][i] = 1

    @property
    def monsters(self):
        return [element for element in self.elements if isinstance(element, character.Monster)]

    def make_order(self) -> list:
        [elements.append(room) for room in self.allrooms]
        [elements.append(wall) for wall in self.border + self.walls]
        elements.append(self.start_room)
        [elements.append(door) for door in self.doors]
        elements.append(self.player)


    def _draw(self, tilesize=None):
        """The draw and update method for the dungeon
        """
        elements = self.make_order()

        [element.draw(tilesize) for element in elements]
        self.player.update()
