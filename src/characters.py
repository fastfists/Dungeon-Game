''' Where I put all of my game classes at (Player, Zombie, Boss) '''
from time import sleep
import pygame
import utils
import classydungeon as dun
import random


class Player(pygame.sprite.Sprite):

    def __init__(self, position, game):
        self.x, self.y = position
        self.health = 100
        self.isAlive = True
        self.game = game
        
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
        self.images = [utils.get_img("Skeleton",x) for x in range(21,30)]
        [image.set_colorkey(utils.BLACK) for image in self.images]
        self.x, self.y = random.choice(self.room.blocks).position
        self.display = self.room.dungeon.game.display
        self.size = dun.Tile.tile_size
        self.direction = 'East'
        self.speed = 0.01
        self.animation_speed = 50
        self.current_frame = 0
        self.state = 0
        self.flip = False

    def show(self):
        temp_img = pygame.transform.scale(self.images[self.state], (self.size,self.size))
        temp_img = pygame.transform.flip(temp_img, self.flip,False)
        self.display.blit(temp_img, (self.x * self.size, self.y * self.size))
        self.current_frame = 0
        self.state += 1
        if self.state > len(self.images) - 1:
            self.state = 0
        
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
            self.flip = False
        else:
            self.x -= self.speed
            self.flip = True



class BossMonster(Monster):

    def __init__(self, room, level):
        self.level = level
        super().__init__(room, health = 100)
        self.image = utils.get_img('Skeleton',34)
        self.image.set_colorkey(utils.BLACK)

