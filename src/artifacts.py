"""This contains any artifacts such as:
   - Projectiles
   - Chests

"""

#import dungeon_utils
import pygame
import collections
import numpy as np
from dungeon_utils import DungeonElement 

stored_class = collections.namedtuple("stored_class",['inst', 'end_cond', 'start_time'])
class Emitter():
    """ A class a dungeon element to the screen and has it disappear
    :param element: Element class that is to be instancitated, element arguments for the instance
    The element class must have draw and update methods
    
    It also recieves a dungeon_utils stop_condition, this is a function that it will call to stop the bliting
    this shouod return True if it wants to end the drawing else false
    leave *args **kwargs for the update adn draw functions to give flexibility to the parents

    The final positional argument is the ammount of frames between each 
    """
    x:int
    y:int
    def __init__(self, element, stop_condition, *element_args, **element_kwargs):        
        if not hasattr(element,'update') or not hasattr(element, 'draw'):
            raise NotImplementedError("Need to add an update and draw method to this class")
        self.element = lambda *args, **kwargs: element(*element_args, *args, **element_kwargs, **kwargs) ## returns a new class instance
        self.stop_condition = stop_condition
        self.elements = []

    def queue(self, *args, stop_condition=None, **kwargs):
        """
        Adds an element additional element arguments
        can be added
        """

        if not stop_condition:
            stop_condition = self.stop_condition
            if not stop_condition:
                raise AttributeError("Missing stop_condition")
        ## TODO  Make a stopper
        self.elements.append(stored_class(self.element(*args, **kwargs), stop_condition, pygame.time.get_ticks()))

    @property
    def elements_instances(self):
        return [element.inst for element in self.elements]

    def update(self, *args, **kwargs):
        """Updates and removes any elements as well as the timer
        Needs to be called every frame"""
        [element.update() for element in self.elements_instances]

        ## calls each of the conditions and if the end condition is there it is deleted
        self.elements = [element for element in self.elements if element.end_cond(element.inst, *args, **kwargs)]

    def emit(self, all=True):
        """ Draws all elements to the screen"""
        [element.draw() for element in self.elements_instances]


class Projectile(DungeonElement, pygame.sprite.Sprite):

    """Object that moves and is deleted on a condition
    Has to have a dungeon element that controls it
    """
    def __init__(self, start_pos:tuple, image: pygame.Surface.Surface, master:DungeonElement, speed, direction:tuple):
        self.image = image
        self.speed = speed if type(self.speed) is tuple else speed,speed
        self.rect = self.image.get_rect()
        DungeonElement.__init__(self, start_pos, master.dungeon)
        pygame.sprite.Sprite.__init__(self)
        self.direction = np.array(direction)

    def __repr__(self):
        return "Projcetile object moving {tuple(self.direction)}"

    def update(self):
        pos = np.aray(self.position)
        self.position = tuple(pos+ self.speed * self.direction) 

    def end_if(self):
        pass

if __name__ == '__main__':
    class MockDungeonElement():
        def draw(self):
            print("Drawn")
        
        def update(self, *args, **kwargs):
            print("Updated and moved a bit")
        
        def end_if(self, *args, **kwargs):
            print("Checked and retruned false")
            return False
        
    emmiter = Emitter(MockDungeonElement, MockDungeonElement.end_if)
    emmiter.queue()
    emmiter.emit()
    emmiter.update()
    emmiter.emit()
