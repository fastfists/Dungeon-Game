"""This contains any artifacts such as:
   - Projectiles
   - Chests

"""

#import dungeon_utils
import pygame
import collections
from dungeon_utils import DungeonElement 

stored_class = collections.namedtuple("stored_class",['inst', 'end_cond'])
class Emitter():
    """ A class a dungeon element to the screen and has it disappear
    This recieves an element class that is to be instancitated, element arguments for the instance
    The element class must have draw and update methods
    
    It also recieves adungeon_utils stop_condition, this is a function that it will call to stop the bliting
    this shouod return True if it wants to end the drawing else false
    leave *args **kwargs for the update adn draw functions to give flexibility to the parents

    The final positional argument is the ammount of frames between each 
    """
    x:int
    y:int
    def __init__(self, element, stop_condition, wait_time, *element_args, **element_kwargs):        
        if not hasattr(element,'update') or not hasattr(element, 'draw'):
            raise NotImplementedError("Need to add an update and draw method to this class")
        self.element = lambda : element(*element_args, **element_kwargs) ## returns a new class instance
        self.stop_condition = stop_condition
        self.wait_time = wait_time
        self.elements = []

    def queue(self, *, start_pos:tuple, end_cond):
        """
        We need emiters to draw a sprite for a second ammount of time as well as update them
        """
        ## TODO  Make a stopper
        self.elements.append(sotred_class(self.element(),end_cond) )

    @property
    def elements_instances(self):
        return [element.inst for element in self.elements]

    def update(self, *args, **kwargs):
        [element.update() for element in element in self.elements_instances]

        ## calls each of the conditions and if the end condition is there it is deleted
        self.elements = [element for element in self.elements() if element.cond(element.inst, *args, **kwargs)]

    def emit(self):
        [element.draw() for element in self.elements]
