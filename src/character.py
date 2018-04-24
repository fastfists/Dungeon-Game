"""
More structered implementation
of my sprites
"""
import pygame
import dungeon_utils

class Sprite(dungeon_utils.DungeonElement, pygame.sprite.Sprite):
    '''Containtains all monster sprites that are contained within my dungeon'''
    def __init__(position, room, health):
        DungeonElement.__init__(random.choice(room.blocks).position, room.dungeon) 
        pygame.sprite.Sprite.__init__()
        self.room = room
        self.health = health
        # For the animations
        self.animation_speed = 1 # 0.55 for the player
        self.images = None # Scale each image after I recieve them
        self.state = {'Idle':True,
                      'Walking':False,
                      'Attacking':False,
                      'Dying': False,
                      'Dead': False }
        self.frame = 0
        self.flipped = False
        self.current_frame = 0
        self.isAlive = True
        self.speed = 0.5

    def draw(self):
        self.image = self.images[self.frame]
        self.image = pygame.transform.flip(self.image, False, self.flipped)
        super().draw()

    def update():
        if self.current_state == "Alive":
            keys = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                move_y = self.speed
            if key[pygame.K_UP]:
                move_y = -self.speed
            if key[pygame.K_LEFT]:
                move_x = -self.speed
            if key[pygame.K_RIGHT]:
                move_x = self.speed
            
            self.x += move_x
            self.y += move_y

            if self.dungeon.Idtbl[round(self.x )][round(self.y)] == 1:
                self.x -= move_x
                self.y -= move_y

            self.moved = True if move_x != 0 or move_y != 0 else False
            if move_x + move_y == 0: self.moved = False
            if move_x < 0:
                self.flip = True
            elif move_x > 0:
                self.flip = False
                
            
    def damgage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.isAlive = False
    
    @property
    def current_state(self):
        for key,value in self.state.items():
            if value == True:
                return key
    
    @current_state.setter
    def change_state(self, new_state):
        unchangeable = ['Attacking', 'Dying', 'Dead']
        if new_state in unchangeable:
            return
        self.state[new_state] = True
        for key, value in self.state.items():
            if value and key != new_state:
                value = False
        

class Monster(Sprite):

    @property
    def x_limit(self):
        return (self.room.blocks[0].x, self.room.blocks[-1].x)

    @property
    def y_limit(self):
        return (self.room.blocks[0].y, self.room.blocks[-1].y)

    def move(self):
        if self.x >= self.x_limit[1]:
            self.direction = 'West'
        elif self.x <= self.x_limit[0]:
            self.direction = 'East'

        if self.direction == 'East':
            self.x += self.speed
            self.flip = False
        elif self.direction == 'West':
            self.x -= self.speed
            self.flip = True


class Skeleton(Monster):
    size = super().size // 4


class Player(Sprite):
    pass

