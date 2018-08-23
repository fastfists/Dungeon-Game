from . import TextButton
import pygame
import numpy as np
from . import utils
from typing import List

class Menu(pygame.sprite.Group):
    """
    Recives a screen size and a 
    dictionary of the variable name and text to display 
    to create a pygame.Group menu 
    """
    def __init__(self, screen_size:tuple, button_names:dict, font_size=32):
        WIDTH, HEIGHT = screen_size

        Gap = MenuCentered(screen_size, font_size, len(button_names))
        for pos, button_text in zip(Gap, button_names.items()):
            var, disp = button_text
            print(button_text)
            exec(f"self.{var} = TextButton(pos, '{disp}')")
        print(self.__dict__)
        super().__init__(*self.__dict__.values())


class MenuCentered:
    """
    Generator class that provides x and y
    coordinates for 
    """
    def __init__(self, screen_size: tuple, gap_size, item_count:int):
        self.item_count = item_count
        self.WIDTH, self.HEIGHT = screen_size
        self.gap_size = gap_size
        self.current = 0
        self.gen = iter(self.modify())

    def modify(self):
        skip_0 = True if self.item_count % 2 == 0 else False
        for i in np.arange((self.item_count- 1) * -0.5, self.item_count):
            if i == 0 and skip_0:
                continue
            yield i
        raise StopIteration

    def __call__(self):
        return next(self)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.item_count:
            x = self.WIDTH // 2
            y = (self.HEIGHT // 2) + (self.gap_size * next(self.gen))
            self.current += 1
            return x, y
        raise StopIteration