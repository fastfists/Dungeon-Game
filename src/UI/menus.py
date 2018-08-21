from . import TextButton
import pygame
import numpy as np
from . import utils


class PauseMenu(pygame.sprite.Group):
    font_size = 32

    def __init__(self, screen_size:tuple, *a, **kw):
        self.width, self.height = WIDTH, HEIGHT = screen_size
        font_size = 32

        Gap = MenuCentered(screen_size, font_size, 4)
        self.resume_button = TextButton(Gap(), "Resume")
        self.options_button = TextButton(Gap(), "Options")
        self.restart_button = TextButton(Gap(), "Restart")
        self.quit_button = TextButton(Gap(), "Quit")
        super().__init__(self.resume_button, self.options_button, self.restart_button, self.quit_button)
        
class EndGameMenu(pygame.sprite.Group):

    def __init__(self, screen_size:tuple, *args, **kwargs):
        WIDTH, HEIGHT = screen_size
        font_size = 32
        Gap = MenuCentered(screen_size, font_size, 2)
        self.quit_button = TextButton(Gap(), "Close")
        self.new_game_button = TextButton(Gap(), "Play Again?")


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
