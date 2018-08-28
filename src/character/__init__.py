import pygame
from src.dungeon_utils import DungeonElement
from contextlib import contextmanager
import src.utils as utils
import src.artifacts as artifacts
import numpy as np
from .healthbar import HealthBar

class Sprite(pygame.sprite.Sprite):
    """
    The sprite abstract class
    handles the animation and changing
    of states for a sprite object
    """
    max_health = 100
    health = 100
    possible_states = {"Idle",
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
            self._images = utils.get_all_images(self.__class__.__name__)  # returns a dict
        self._images["Dead"] = [self._images["Dying"][-1]]  # passes the last index
        self.health = HealthBar(self.health, self.max_health, self.image.get_rect().width)

    def __init_subclass__(cls, picture_name: str = None, **kwargs):
        if picture_name:
            cls._images = utils.get_all_images(picture_name)
        super().__init_subclass__(**kwargs)

    def animate(self):
        """ Changes the frame of the image """
        if not self.dead:
            self.counter += self.animation_speed
            if self.counter >= 1:
                # Changes to another image/frame
                self.counter = 0
                self.frame += 1
                if self.frame > len(self.images) - 1:
                    # Resets the complete animation
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

    def damage(self, dmg):
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

    def __hash__(self):
        return pygame.sprite.Sprite.__hash__(self)


class Monster(Sprite, DungeonElement):

    def __init__(self, room, position=None):
        self.room = room
        if not position:
            position = random.choice(self.room.blocks).position
        Sprite.__init__(self)  # Calls the sprite class
        DungeonElement.__init__(self, position, self.room.dungeon)
        self.image.set_colorkey(utils.BLACK)

    def draw(self, *a, **kw):
        if not self.dead:
            super().draw(*a, **kw)
            self.health.draw_bar(self.display, self.rect)

    def update(self):
        if not self.dead:
            super().animate()
            self.image.set_colorkey(utils.BLACK)

    def damage(self, *a, **kw):
        super().damage(*a, **kw)
        state = self.state
        if state == "Dying" or state == "Dead":
            self.room.check_if_cleared()


@contextmanager
def collides_with(self, class_name="any_sprite", group=None):
    """
    A context manager that returns what it collides with
        :param self: Any object that is in dungeon elements and has a rectangle
        :param class_name="any_sprite": Defaulted to any sprite, can be changed by adding a sprite class
    """
    group = self.dungeon.elements if not group else group
    collides = pygame.sprite.spritecollide(self, group, False)
    if collides and class_name != "any_sprite":
        collides = [sprite for sprite in collides if isinstance(sprite, class_name)]
    yield collides

from .monsters import *
from .player import *
