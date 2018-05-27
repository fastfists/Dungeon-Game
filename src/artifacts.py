"""This contains any artifacts such as:
   - Projectiles
   - Chests

"""

#import dungeon_utils
import pygame
import collections
import numpy as np
import utils
from dungeon_utils import DungeonElement 

stored_class = collections.namedtuple("stored_class",['inst', 'end_cond', 'start_time'])
class Emitter():
    """ A class a dungeon element to the screen and has it disappear
    :param element: Element class that is to be instancitated, element arguments for the instance
    The element class must have draw and update methods
    
    It also recieves a dungeon_utils stop_condition, this is a function that it will call to stop the bliting
    this shouod return True if it wants to end the drawing else false
    leave *args **kwargs for the update adn draw functions to give flexibility to the parents

    One optional argument is the ammount of frames between each iteration that is allowed 
    """

    def __init__(self, element, stop_condition, cooldown=25, element_args=[], element_kwargs={}):        
        if not hasattr(element,'update') or not hasattr(element, 'draw'):
            raise NotImplementedError("Need to add an update and draw method to this class")
        self.element = lambda *args, **kwargs: element(*element_args, *args, **element_kwargs, **kwargs) ## returns a new class instance
        self.stop_condition = stop_condition
        self.elements = []
        self.frames_passed = 0
        self.frame_limit = cooldown

    @property
    def ready(self):
        return self.frames_passed >= self.frame_limit

    def load(self, additional_args=[], stop_condition=None, additional_kwargs={}):
        """
        Adds an element additional element arguments can be added before construction of the arugment such as an x and y value
        """
        if self.ready:
            if not stop_condition:
                stop_condition = self.stop_condition
                if not stop_condition:
                    raise AttributeError("Missing stop_condition")
            ## TODO  Make a stopper
            self.elements.append(stored_class(self.element(*additional_args, **additional_kwargs), stop_condition, pygame.time.get_ticks()))
            self.frames_passed = 0

    def __repr__(self):
        return f"Emmiter object with {len(self.elements)} objects"

    @property
    def elements_instances(self):
        return [element.inst for element in self.elements]

    def update(self, cond_args=[], cond_kwargs={}):
        """Updates and removes any elements as well as the timer
        Needs to be called every frame
        Also recieves args that can be passed to the element"""

        [element.update() for element in self.elements_instances]
        self.frames_passed +=1
        ## calls each of the conditions and if the end condition is there it is deleted
        self.elements = [element for element in self.elements if element.end_cond(element.inst, *cond_args, **cond_kwargs)]

    def emit(self, all=True):
        """ Draws all elements to the screen"""
        [element.draw() for element in self.elements_instances]


class Projectile(DungeonElement, pygame.sprite.Sprite):

    """Object that moves and is deleted on a condition
    Has to have a dungeon element that controls it
    treat Projectiles as vectors
    The direction parameter is a tuple value with the first
    value being the x direction and the second is the y direction
    """
    def __init__(self, *, start_pos:tuple, image, master:DungeonElement, speed:float, direction:tuple, max_dist=5):
        self.speed = speed if type(speed) is tuple else speed,speed
        self.image = image
        self.image.set_colorkey(utils.BLACK)
        self.rect = self.image.get_rect()
        DungeonElement.__init__(self, start_pos, master.dungeon) ## init surface and x, y
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.start_pos = self.position
        pygame.sprite.Sprite.__init__(self)
        self.direction = np.array(direction)
        self.dead = False
        self.flip = self.direction[0] < 0
    def __repr__(self):
        return "Projcetile object moving {tuple(self.direction)}"

    def draw(self, *args, **kwargs):
        super().draw(*args, **kwargs, flip=self.flip)

    def update(self):
        pos = np.array(self.position)
        print(type(self.x))
        print('before:', self.position, end="after: ")
        self.position = (pos + (self.speed * self.direction)).tolist()
        print(type(self.x))
        x, y = self.graph_position
        if self.dungeon.Idtbl[x][y] == 1:
            self.dead = True
            self.kill()

    def end_if(self):
        return not self.dead
        

if __name__ == '__main__':
    class MockDungeonElement():
        def draw(self):
            print("Drawn")
        
        def update(self, *args, **kwargs):
            print("Updated and moved a bit")
        
        def end_if(self, *args, **kwargs):
            print(args, kwargs)
            print("Checked and returned false")
            return False
    
    emmiter = Emitter(MockDungeonElement, MockDungeonElement.end_if)
    emmiter.load()
    emmiter.emit()
    emmiter.update() ## calls both end_if and update methods
    emmiter.emit()
