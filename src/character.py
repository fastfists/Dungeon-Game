"""
More structered implementation
of my sprites
"""
import pygame
from dungeon_utils import DungeonElement 

class Sprite(pygame.sprite.Sprite):
    '''
    The sprite abstract class
    handles the animation and changing 
    of states for a sprite object
    '''
    health = 100
    states = []
    default_state = 'idle'
    animation_speed = 1
    images = NotImplemented
    image = NotImplemented
    speed = 0.5
    frame = 0
    counter = 0
    def __init__(self):
        self._state = {default_state:True}
        for option in self.states:
            if option == default_state:
                continue
            self._state[option] = False
        del states

    def __repr__(self):
        return super().__repr__() + " I am also a sprite"

    def animate(self):
        """ Changes the frame of the image """
        self.image = self.images[self.frame]
        self.counter += self.animation_speed
        if counter > 1:
            counter = 0
            self.frame = (self.frame + 1) % len(self.images)

    def reset_animations(self):
        self.frame, self.counter = 0,0

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
            self.reset_animations()
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

    def draw(self):
        super().animate()
        super().draw()

    def patrol(self):
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
    pass


class Player(Sprite):
    pass

