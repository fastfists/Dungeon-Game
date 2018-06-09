"""More structered implementation
of my sprites
"""
import pygame
import random
import utils
import artifacts
import json
from os import path
from dungeon_utils import DungeonElement
from contextlib import contextmanager


class Sprite(pygame.sprite.Sprite):
    """
    The sprite abstract class
    handles the animation and changing
    of states for a sprite object
    """
    def __hash__(self):
        return pygame.sprite.Sprite.__hash__(self)
    
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
    _end = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # create the _state instance
        self._state = {self.default_state: True}
        for option in self.possible_states | self.unstopable_states:
            if option == self.default_state:
                continue
            self._state[option] = False
        if not hasattr(self, "_images"):
            self._images = utils.get_all_images(self.__class__.__name__) # returns a dict
        self._images["Dead"] = [self._images["Dying"][-1]] # passes the last index

    def __init_subclass__(cls, picture_name:str= None, **kwargs):
        if picture_name:
            cls._images = utils.get_all_images(picture_name)
        super().__init_subclass__(**kwargs)

    def animate(self):
        """ Changes the frame of the image """
        if not self.dead:
            self.counter += self.animation_speed
            if self.counter >= 1:
                self.counter = 0
                self.frame += 1
                if self.frame > len(self.images) - 1:
                    if self.state in self.unstopable_states:
                        if self.state == "Dying":
                            super().kill()
                            with self.end_of_animation():
                                self.state = "Dead"
                        else:
                            with self.end_of_animation():
                                self.state = self.default_state
                    self.reset_animations()

    @property
    def dead(self):
        return self.state == "Dead"

    @contextmanager
    def end_of_animation(self):
        self._end = True
        yield
        self._end = False

    def reset_animations(self):
        """Sets the frame counters to 0"""
        self.frame, self.counter = 0, 0

    def damgage(self, dmg):
        """ Reduces the health"""
        self.health -= dmg
        if self.health <= 0:
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
        self.image.set_colorkey(utils.BLACK)

    def update(self):
        if not self.dead:
            super().animate()
            self.image.set_colorkey(utils.BLACK)


class Skeleton(Monster):
    default_state = 'Walk'
    possible_states = {'Walk', 'Attack'}
    animation_speed = 0.88
    speed = 0.03
    flip = False

    def __init__(self, *args, **kwargs):
        self.direction = random.choice(['West', 'East'])
        super().__init__(*args, **kwargs)

    def draw(self, *args, **kwargs):
        super().draw(*args, flip=self.flip, **kwargs)

    @property
    def x_limit(self):
        return self.room.blocks[0].x, self.room.blocks[-1].x

    @property
    def y_limit(self):
        return self.room.blocks[0].y, self.room.blocks[-1].y

    def update(self, active:bool):
        if not self.dead:
            super().update()
            if active:
                self.state = "Walk"
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
                
            else:
                self.state = "Idle"

class BossSkeleton(Skeleton, picture_name="Skeleton"):
    def __init__(self, *args,level=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_skeletons = self.levels(level)
        self.size *= 8
        self.size //= 2
        self.skelton_spawner = artifacts.Emitter(Skeleton, lambda skel: skel.state != 'Dead', cooldown=50, element_args=[self.room], element_kwargs={"delay":7})
        self.health = 200

    @staticmethod
    def levels(level:int) -> int:
        """ Method that returns the limit of skeletons to spawn based on level """
        with open(path.join(utils.db,"boss_skeleton.json")) as f:
            data = json.load(f)
            return data[f"Level {level}"]

    def draw(self, *args, **kwargs):
        super().draw()
        self.skelton_spawner.emit()

    def update(self, active):
        super().update(active)
        if active and not self.dead:
            if len(self.skelton_spawner) != self.max_skeletons:
                if self.skelton_spawner.ready:
                    self.state = "Attacking"
                    x,y = self.position
                    start_pos = x + random.uniform(.5,.10), y + random.uniform(.5,.10)
                    self.skelton_spawner.load(additional_kwargs={'position':start_pos})
            self.skelton_spawner.update(active)
            self.dungeon.elements.add(self.skelton_spawner[-1])
        self.skelton_spawner.update(active)


class Player(Sprite, DungeonElement, picture_name="Rouge"):
    animation_speed = 0.33
    speed = 0.1
    x:float
    y:float
    flip = False
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.position = dungeon.start_pos
        Sprite.__init__(self)
        DungeonElement.__init__(self, self.position, self.dungeon)
        self.size *= 4
        self.size //= 5
        weapon_dict = dict(master=self, image=utils.get_single_img('sword_slash'), speed=self.speed *3, delay=20)
        self.shooter = artifacts.Emitter(artifacts.Projectile, artifacts.Projectile.end_if, element_kwargs=weapon_dict, cooldown=25)

    def update(self):
        self.get_keys()
        self.shooter.update()

    def draw(self, *args, **kwargs):
        super().animate()
        self.image.set_colorkey(utils.BLACK)
        self.shooter.emit()
        super().draw(*args, flip=self.flip, **kwargs)

    def get_keys(self):
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

        #########################
        #      Get actions      #
        #########################
        direction = (-1,0) if self.flip else (1,0)
        if key[pygame.K_SPACE] and self.shooter.ready:
            self.state = 'Attacking'
            self.shooter.load(additional_kwargs=dict(start_pos=self.position, direction=direction))
