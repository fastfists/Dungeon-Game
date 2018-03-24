''' Where I put all of my game classes at (Player, Zombie, Boss) '''
from time import sleep
import pygame
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
        self.speed = 0.08
        
        self.move_images = [utils.get_img("Rouge",x) for x in range(21,30)]
        self.idle_images = [utils.get_img("Rouge",x) for x in range(1,10)]
        self.death_images = [utils.get_img("Rouge",x) for x in range(41,50)]
        self.attack_images = [utils.get_img("Rouge",x) for x in range(21,30)]
        self.current_frame = 0
        self.animation_speed = 0.5 # goes half as fast as the framerate

        [image.set_colorkey(utils.BLACK) for image in self.move_images]
        [image.set_colorkey(utils.BLACK) for image in self.idle_images]
        [image.set_colorkey(utils.BLACK) for image in self.death_images]
        [image.set_colorkey(utils.BLACK) for image in self.attack_images]

        self.size = dun.Tile.tile_size
        self.display = game.display
        self.state = 0
        self.flip = False
        self.moved = False

    def show(self):
        # TODO rethink this method in terms of changing states
        if self.moved:
            image_array = self.move_images
        else:
            image_array = self.death_images
        temp_img = pygame.transform.scale(image_array[self.state], (self.size,self.size))
        temp_img = pygame.transform.flip(temp_img, self.flip,False)
        self.display.blit(temp_img, (self.x * self.size, self.y * self.size))
        self.current_frame += self.animation_speed
        if self.current_frame >= 1:
            self.state += 1
            self.current_frame = 0
            if self.state > len(image_array) - 1:
                self.state = 0


    def attack(self):
        print("charge")
    
    def update(self):
        pass

    def move(self,xChange=0, yChange=0):
        if xChange: self.x += xChange * self.speed
        if  yChange: self.y += yChange * self.speed
        if xChange + yChange != 0: self.moved = True

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

        self.images = [utils.get_img("Skeleton",x) for x in range(21,30)]
        [image.set_colorkey(utils.BLACK) for image in self.images]

        self.x, self.y = random.choice(self.room.blocks).position
        self.display = self.room.dungeon.game.display
        self.size = dun.Tile.tile_size
        self.direction = random.choice(['East', 'West'])
        self.speed = 0.01
        self.animation_speed = 0.33 # goes half as fast as the framerate
        self.current_frame = 0
        self.state = 0
        self.flip = False

    def show(self):
        temp_img = pygame.transform.scale(self.images[self.state], (self.size,self.size))
        temp_img = pygame.transform.flip(temp_img, self.flip,False)
        self.display.blit(temp_img, (self.x * self.size, self.y * self.size))
        self.current_frame += self.animation_speed
        if self.current_frame >= 1:
            self.state += 1
            self.current_frame = 0
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
        if self.x >= self.x_limit[1]:
            self.direction = 'West'
        elif self.x <= self.x_limit[0]:
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

