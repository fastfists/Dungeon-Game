''' Where I put all of my game classes at (Player, Zombie, Boss) '''

import classydungeon as dun

class Player:
    def __init__(self, xStart, yStart):
        self.x = xStart
        self.y = yStart
        self.health = 100
        self.isAlive = True
    
    def show(self):
        print('hello')
    
    def shoot(self):
        print("pew")
    
    def move(self,xChange=0, yChange=0):
        self.x += xChange
        self.y += yChange

    def hit(self, dmg):
        self.health -= dmg


class Monster:
    def __init__(self, room, health = 50):
        self.room = room
        self.health = health
        self.isAlive = None
        #self.picture = 'zombie.png' 

    @property
    def x_limit(self):
        ''' Returns a tuple containing (x min x max) '''
        return (self.room.blocks[0].get_x(), self.room.blocks[-1].get_x())

    @property
    def y_limit(self):
        return (self.room.blocks[0].get_y(), self.room.blocks[-1].get_y())

    def attack(self):
        pass

    def damgage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.isAlive = False
    
    def show(self):
        """
        Draws self using the X and Y position
        """
        if not isAlive:
            return
        # It is alive Draw
        pass

    def patrol(self):
        if self.x > self.x_limit[1]:
            self.direction = 'West'
        elif self.x < self.x_limit[0]:
            self.direction = 'East'

        if self.direction = 'East':
            self.x += .1
        else:
            self.x -= .1


class Boss(Monster):

    def __init__(self, room, level):
        self.level = level
        super().__init__(room, health = 100)


if __name__ == '__main__':
    boi = dun.dungeon()
    boi.make()
    boi.draw()
    print("?")
