"""
More structered implementation
of my sprites
"""
import pygame
import dungeon_utils

class Sprite(pygame.sprite.Sprite):
    '''Containtains all monster sprites that are contained within my dungeon'''
    health = 100
    _state = {'Idle':True,
            'Walking':False,
            'Attacking':False,
            'Dying': False,
            'Dead': False }
    animation_speed = 1
    images = NotImplemented
    image = NotImplemented
    speed = 0.5
    frame = 0
    
    def animate(self):
        """ Changes the frame of the image """
        self.image = self.images[self.frame]
        self.frame = (self.frame + 1) % len(images)

    def damgage(self, dmg):
        """ Reduces the health"""
        self.health -= dmg
        if self.health < 0:
            self.state = "Dying"

    @property
    def state(self):
        for key,value in self.state.items():
            if value == True:
                return key
    
    @ state.setter
    def change_state(self,new_state):
        if not new_state in ['Attacking', 'Dying', 'Dead']:
            self._state[new_state] = True
            for key, value in self._state.items():
                if value and key != new_state:
                    value = False


class Monster(Sprite, dungeon_utils.DungeonElement):
    def __init__(self, room):
        self.room = room


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

