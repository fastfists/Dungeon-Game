"""
More structered implementation
of my sprites
"""
import pygame
import random
import utils
from dungeon_utils import DungeonElement 


class Sprite(pygame.sprite.Sprite):
    '''
    The sprite abstract class
    handles the animation and changing 
    of states for a sprite object
    '''
    health = 100
    possible_states = ['Idle',
              'Emote',
              'Walk',
              'Attack',
              'Death']
    default_state = 'Idle'
    animation_speed = 1
    speed = 0.5
    frame = 0
    counter = 0


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # create the _state instance
        self._state = {self.default_state:True}
        for option in self.possible_states:
            if option == self.default_state:
                continue
            self._state[option] = False

        self._images = utils.get_all_images(self.__class__.__name__)


    def __repr__(self):
        return super().__repr__() + " I am also a sprite"

    def animate(self):
        """ Changes the frame of the image """
        self.counter += self.animation_speed
        if self.counter >= 1:
            counter = 0
            self.frame += 1
            if self.frame > len(self.images)- 1:
                self.frame = 0


    def reset_animations(self):
        """Sets the frame counters to 0"""
        self.frame, self.counter = 0,0

    def damgage(self, dmg):
        """ Reduces the health"""
        self.health -= dmg
        if self.health < 0:
            self.state = "Dying"

    @property
    def state(self) -> str:
        for key,value in self._state.items():
            if value:
                return key
    
    @ state.setter
    def state(self,new_state):
        print("Changing state")
        if not new_state in ['Attacking', 'Dying', 'Dead']:
            self._state[new_state] = True
            self.reset_animations()
            for key, value in self._state.items():
                if value and key != new_state:
                    value = False


    @property
    def image(self) -> pygame.surface.Surface:
        return self.images[self.frame]
    
    @image.setter
    def image(self, new_image: pygame.surface.Surface):
        self.images[self.frame] = new_image

    @property
    def images(self) -> list:
        return self._images[self.state]


class Person(Sprite, DungeonElement):
    
    def __init__(self, room):
        self.room = room
        Sprite.__init__(self) # Calls the sprite class
        DungeonElement.__init__(self, random.choice(self.room.blocks).position, self.room.dungeon)

    def draw(self, *args, **kwargs):
        super().animate()
        self.image.set_colorkey(utils.BLACK)
        super().draw(*args, **kwargs)

    def activate(self):
        pass


class Skeleton(Person):
    default_state = 'Walk'
    possible_states = ['Walk']
    animation_speed = 0.005
    speed = 0.01
    flip = False
    def __init__(self, *args, **kwargs):
        self.direction = random.choice(['West','East'])
        super().__init__(*args, **kwargs)

    def draw(self,*args, **kwargs):
        super().draw(*args, flip=self.flip ,**kwargs)

    @property
    def x_limit(self):
        return (self.room.blocks[0].x, self.room.blocks[-1].x)

    @property
    def y_limit(self):
        return (self.room.blocks[0].y, self.room.blocks[-1].y)

    def activate(self):
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


class Player(Person):
    pass

