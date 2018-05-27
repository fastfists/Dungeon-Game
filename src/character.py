"""More structered implementation
of my sprites
"""
import pygame
import random
import utils
import artifacts
from dungeon_utils import DungeonElement


class Sprite(pygame.sprite.Sprite):
    """
    The sprite abstract class
    handles the animation and changing
    of states for a sprite object
    """
    health = 100
    possible_states =  {"Idle",
                        "Emote",
                        "Walk",
                        "Death"}
    default_state = "Idle"
    animation_speed = 1
    speed = 0.5
    frame = 0
    counter = 0
    unstopable_states = {"Attacking",
                         "Dying",
                         "Dead"}
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # create the _state instance
        self._state = {self.default_state: True}
        for option in self.possible_states | self.unstopable_states:
            if option == self.default_state:
                continue
            self._state[option] = False
        self._images = utils.get_all_images(self.__class__.__name__) # returns a dict
        self._end = False

    def __repr__(self):
        return super().__repr__()

    def animate(self):
        """ Changes the frame of the image """
        self.counter += self.animation_speed
        if self.counter >= 1:
            self.counter = 0
            self.frame += 1
            if self.frame > len(self.images) - 1:
                if self.state in self.unstopable_states:
                    self._end = True
                    self.state = self.default_state
                    self._end = False
                self.reset_animations()
                
    def reset_animations(self):
        """Sets the frame counters to 0"""
        self.frame, self.counter = 0, 0

    def damgage(self, dmg):
        """ Reduces the health"""
        self.health -= dmg
        if self.health < 0:
            self.state = "Dying"

    @property
    def state(self) -> str:
        for key, value in self._state.items():
            if value:
                return key

    @state.setter
    def state(self, new_state):
        if (not self.state in self.unstopable_states and self.state != new_state) or self._end:
            self.reset_animations()
            for key in self._state.keys():
                self._state[key] = False
            self._state[new_state] = True

    @property
    def images(self):
        return self._images[self.state]

    @property
    def rect(self):
        return self.image.get_rect()


    @property
    def image(self) -> pygame.surface.Surface:
        return self.images[self.frame]

    @image.setter
    def image(self, new_image: pygame.surface.Surface):
        self.images[self.frame] = new_image


class Monster(Sprite, DungeonElement):

    def __init__(self, room, position=None):
        self.room = room
        if not position:
            position = random.choice(self.room.blocks).position
        Sprite.__init__(self)  # Calls the sprite class
        DungeonElement.__init__(self, position, self.room.dungeon)

    def draw(self, *args, **kwargs):
        super().animate()
        self.image.set_colorkey(utils.BLACK)
        super().draw(*args, **kwargs)

    def activate(self):
        pass


class Skeleton(Monster):
    unstopable_states = set()
    default_state = 'Walk'
    possible_states = {'Walk', 'Attack'}
    animation_speed = 0.88
    speed = 0.03
    flip = False

    def __init__(self, *args, **kwargs):
        self.direction = random.choice(['West', 'East'])
        super().__init__(*args, **kwargs)
        self.size //= 4
        self.size *=2

    def draw(self, *args, **kwargs):
        super().draw(*args, flip=self.flip, **kwargs)

    @property
    def x_limit(self):
        return self.room.blocks[0].x, self.room.blocks[-1].x

    @property
    def y_limit(self):
        return self.room.blocks[0].y, self.room.blocks[-1].y

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
        
        choice = random.choice([self.speed, -self.speed])
        self.y += choice
        if self.y < self.y_limit[0] or self.y > self.y_limit[1]:
            # if out of bounds
            self.y -= choice



class BossSkeleton(Skeleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size *=4
        self.size //=3


class Player(Sprite, DungeonElement):
    animation_speed = 0.33
    speed = 0.05
    x:float
    y:float
    flip = False
    def __init__(self, dungeon):
        self.position = dungeon.start_pos
        self.dungeon = dungeon
        Sprite.__init__(self)
        DungeonElement.__init__(self, self.position, self.dungeon)
        self.size //= 5
        self.size*=4
        weapon_dict = dict(master=self, image=utils.get_whole_img('sword_slash'))
        self.shooter = artifacts.Emitter(artifacts.Projectile, artifacts.Projectile.end_if, element_kwargs=weapon_dict)

    def update(self):
        self.get_keys()
        self.shooter.update()
    
    def draw(self, *args, **kwargs):
        super().animate()
        self.image.set_colorkey(utils.BLACK)
        super().draw(*args, flip=self.flip, **kwargs)
        #self.shooter.emit()

    def get_keys(self):
        """
        Moves the Charcter across the board
        TODO fix the changing of states to match my better one
        """
        key = pygame.key.get_pressed()
        #########################
        #  Moving of character  #
        #########################
        move_x, move_y = 0,0
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
        if move_x != 0 or move_y != 0:
            self.state = 'Walk'
        else:
            self.state = 'Idle'
        if move_x < 0:
            self.flip = True
        elif move_x > 0:
            self.flip = False

        #################
        #  Get actions  #
        #################
        if key[pygame.K_SPACE]:
            self.state = 'Attacking'
            self.shooter.load(additional_kwargs=dict(start_pos=self.position, speed=self.speed, direction=(1,0)))
