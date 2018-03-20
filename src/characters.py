''' Where I put all of my game classes at (Player, Zombie, Boss) '''
try:
    from game import *
except ImportError: pass
try:
    from classydungeon import Room
except ImportError: pass
try:
    import pygame
except ImportError: pass

class Player(pygame.sprite.Sprite):
    #TODO dont forget to extend this class as a sprite
    def __init__(self, xStart, yStart):
        self.x = xStart
        self.y = yStart
        self.health = 100
        self.isAlive = True
    
    def show(self):
        print('hello')
    
    def attack(self):
        print("charge")
    
    def move(self,xChange=0, yChange=0):
        self.x += xChange
        self.y += yChange

    def hit(self, dmg):
        self.health -= dmg


class Monster(pygame.sprite.Sprite):
    ''' The main enemy Mob spawn  '''
    # TODO abstract this class later on to create new mobs
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

    def patrol(self):
        if self.x > self.x_limit[1]:
            self.direction = 'West'
        elif self.x < self.x_limit[0]:
            self.direction = 'East'

        if self.direction == 'East':
            self.x += self.speed
        else:
            self.x -= self.speed


class BossMonster(Monster):

    def __init__(self, room, level):
        self.level = level
        super().__init__(room, health = 100)


if __name__ == '__main__':
    boi = dungeon()
    boi.make()
    boi.draw()