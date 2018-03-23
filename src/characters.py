''' Where I put all of my game classes at (Player, Zombie, Boss) '''


try:
    import pygame
except ImportError as e:print(e)
import utils
import classydungeon as dun
import random


class Player(pygame.sprite.Sprite):

    def __init__(self, position, game):
        self.x, self.y = position
        print(self.x, self.y)
        self.health = 100
        self.isAlive = True
        self.game = game
        self.speed = 0.05
        self.image = utils.get_img("Rouge",1)
        self.image.set_colorkey(utils.BLACK)
        self.size = dun.Tile.tile_size
        self.display = game.display

    def show(self):
        temp_img = pygame.transform.scale(self.image, (self.size,self.size)) 
        self.display.blit(temp_img, (self.x * dun.Tile.tile_size , self.y * dun.Tile.tile_size ))

    def attack(self):
        print("charge")
    
    def move(self,xChange=0, yChange=0):
        if xChange: self.x += xChange * self.speed
        if  yChange: self.y += yChange * self.speed

    def hit(self, dmg):
        self.health -= dmg


class Monster(pygame.sprite.Sprite):
    ''' The main enemy Mob spawn  '''
    speed = 0.01
    # TODO abstract this class later on to create new mobs
    def __init__(self, room, health = 50):
        self.room = room
        self.health = health
        self.isAlive = None
        self.image = utils.get_img("Skeleton", 5)
        self.image.set_colorkey(utils.BLACK)
        self.x, self.y = random.choice(self.room.blocks).position
        self.display = self.room.dungeon.game.display
        self.size = dun.Tile.get_tile_size()
        self.direction = 'East'


    def show(self):
        temp_img = pygame.transform.scale(self.image, (self.size,self.size)) 
        self.display.blit(temp_img, (self.x * dun.Tile.tile_size, self.y * dun.Tile.tile_size))

    @property
    def x_limit(self):
        ''' Returns a tuple containing (x min x max) '''
        return (self.room.blocks[0].x, self.room.blocks[-1].x)

    @property
    def y_limit(self):
        return (self.room.blocks[0].y, self.room.blocks[-1].y)

    def attack(self):
        pass

    def damgage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.isAlive = False

    def show_health_bar(self):
        pass

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
        self.image = utils.get_img('Skeleton',34)
        self.image.set_colorkey(utils.BLACK)
