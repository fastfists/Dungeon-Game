"""This contains any artifacts such as:
   - Projectiles
   - Chests
"""
import collections
import json
from os import path

import numpy as np
import pygame

import character
import utils
from dungeon_utils import DungeonElement

stored_class = collections.namedtuple("stored_class", ['inst', 'end_cond', 'start_time'])


class Emitter():
    """ A class a dungeon element to the screen and has it disappear
    : param element: Element class that is to be instantiated, element arguments for the instance
    The element class must have draw and update methods
    
    It also recieve a dungeon_utils stop_condition, this is a function that it will call to stop the bliting
    this should return True if it wants to end the drawing else false
    leave *args **kwargs for the update adn draw functions to give flexibility to the parents

    One optional argument is the amount of frames between each iteration that is allowed
    """

    def __init__(self, element, stop_condition, cooldown=25, element_args=[], element_kwargs={}):
        if not hasattr(element, 'update') or not hasattr(element, 'draw'):
            raise NotImplementedError("Need to add an update and draw method to this class")
        self.element = lambda *args, **kwargs: element(*element_args, *args, **element_kwargs,
                                                       **kwargs)  ## returns a new class instance
        self.stop_condition = stop_condition
        self.elements = []
        self.frames_passed = cooldown  # set it to ready first
        self.frame_limit = cooldown

    @property
    def ready(self):
        return self.frames_passed >= self.frame_limit

    def load(self, additional_args=[], stop_condition=None, additional_kwargs={}):
        """
        Adds an element additional element arguments can be added before 
        construction of the arugment such as an x and y value
        """
        if self.ready:
            print("loaded")
            if not stop_condition:
                stop_condition = self.stop_condition
                if not stop_condition:
                    raise AttributeError("Missing stop_condition")
            self.frames_passed = 0
            self.elements.append(stored_class(self.element(*additional_args, **additional_kwargs),
                                              stop_condition, pygame.time.get_ticks()))

    def __repr__(self):
        return f"Emmiter object with {len(self.elements)} objects"

    def __len__(self):
        return len(self.elements)

    @property
    def elements_instances(self):
        return [element.inst for element in self.elements]

    def __getitem__(self, index):
        return self.elements_instances[index]

    def __iter__(self):
        return iter(self.elements_instances)

    def update(self, *update_args, **update_kwargs):
        """Updates and removes any elements as well as the timer
        Needs to be called every frame
        Also recieves args that can be passed to the element for the update"""

        [element.update(*update_args, **update_kwargs) for element in self.elements_instances]
        self.frames_passed += 1
        ## calls each of the conditions and if the end condition is there it is deleted
        new_elements = [element for element in self.elements if element.end_cond(element.inst)]
        [element.inst.kill() for element in self.elements if element not in new_elements]
        self.elements = new_elements

    def emit(self,*draw_args, **draw_kwargs):
        """ Draws all elements to the screen"""
        [element.draw(*draw_args, **draw_kwargs) for element in self.elements_instances]


class Projectile(DungeonElement, pygame.sprite.Sprite):
    """Object that moves and is deleted on a condition
    Has to have a dungeon element that controls it
    treat Projectiles as vectors
    The direction parameter is a tuple value with the first
    value being the x direction and the second is the y direction
    """

    def __init__(self, *, start_pos: tuple, image, master: DungeonElement, 
                 speed: float, direction: tuple, max_dist=5, delay=0):

        self.speed = speed if type(speed) is tuple else speed, speed
        self.image = image
        self.image.set_colorkey(utils.BLACK)
        DungeonElement.__init__(self, start_pos, master.dungeon)  ## init surface and x, y
        self.scale((self.size, self.size))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.start_pos = self.position
        pygame.sprite.Sprite.__init__(self)
        self.direction = np.array(direction)
        self.dead = False
        self.flip = self.direction[0] < 0
        self.image = self.image if not self.flip else pygame.transform.flip(self.image, True, False)
        self.dealy = delay
        self.counter = 0

    @property
    def ready(self):
        return self.dealy <= self.counter

    def __repr__(self):
        emmiter().load()

    def hits(self) -> bool:
        collided = pygame.sprite.spritecollide(self, self.dungeon.elements, False, collided=None)
        kill = False
        if collided:
            for thing in collided:
                if isinstance(thing, character.Monster):
                    kill = True
                    thing.damgage(50)
                    self.dead = True
        if kill: self.kill()

    def draw(self, *a):
        super().draw(*a)

    def update(self):
        if self.ready:
            pos = np.array(self.position)
            self.hits()
            self.position = (pos + (self.speed * self.direction)).tolist()
            x, y = self.graph_position
            if self.dungeon.Idtbl[x][y] == 1:
                self.kill()
        self.counter += 1

    def kill(self):
        super().kill()
        self.dead = True

    def end_if(self):
        return not self.dead


class Chest(DungeonElement):
    """
    The Chest class is a class that only emmits an object once and stays open
    after interacted with
    """

    @classmethod
    def chest_with_health_potion(cls, pos, dungeon):
        class images:
            opened = utils.get_img("Containers", 1)
            closed = utils.get_img("Containers", 2)
        
        return cls(pos, images(), dungeon, Potion.from_db("Health", dungeon, pos))

    def __init__(self, pos: tuple, images: collections.namedtuple, dungeon, *contains):
        self.image = images.closed
        super().__init__(pos, dungeon)
        self.elements = contains
        self.opened = False

    def interact(self):
        if not self.opened:
            self.opened = True
            self.image = self.images.opened

    def draw(self, *a, **kw):
        super().draw(*a, **kw)
        if self.opened:
            for element in self.elements:
                element.draw(*a, **kw)

    def update(self):
        if self.opened:
            for element in self.elements:
                element.update()

class Potion(DungeonElement):

    @classmethod
    def from_db(cls, lookup_name:str, dungeon, pos:tuple):
        f = path.join(utils.db, "Potions", lookup_name+".json")
        result = json.load(open(f))
        result["dungeon"] = dungeon
        result["pos"] = pos
        result["image"] = utils.get_img("Potions", result.pop("lookup_number"))
        return cls(**result)

    def Heal(self, target):
        target.health += self.power

    def Increase_Damage(self, target):
        target.damgage += self.power

    def Increase_Defense(self, target):
        target.debuff += self.power # Not ready to be added

    def update(self):
        with character.collides_with(self, character.Player) as players:
            [getattr(self, effect)(player) for effect in self.effects for player in players]

    def __init__(self, name:str, pos:tuple, dungeon, image=None, effects=[], power=10, Description=""):
        self.image = image
        super().__init__(pos, dungeon)
        self.name = name
        self.power = power
        assert effects, "Effects needed to initialize"
        self.effects = effects
        self.description = Description
        self.size = self.size //2
        self.width = self.height = self.size
        self.image.set_colorkey(utils.BLACK)
        #self.scale(())
        # vairalbes for hover

if __name__ == '__main__':
    class MockDungeonElement:

        def draw(self):
            print("Drawn")

        def update(self, *args, **kwargs):
            print("Updated and moved a bit")

        def end_if(self, *args, **kwargs):
            print(args, kwargs)
            print("Checked and returned false")
            return False


    emmiter = Emitter(MockDungeonElement, MockDungeonElement.end_if, cooldown=0)
    emmiter.load()
    emmiter.emit()
    emmiter.update()  ## calls both end_if and update methods
    emmiter.emit()
