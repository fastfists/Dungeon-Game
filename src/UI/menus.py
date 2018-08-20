from . import TextButton
import pygame


class PauseMenu(pygame.sprite.Group):
    font_size = 32

    def __init__(self, screen_size:tuple, *a, **kw):
        WIDTH, HEIGHT = screen_size
        font_size = 32

        Gap = MenuCentered(screen_size, font_size, 4)
        self.resume_button = TextButton(Gap(), "Resume")
        self.options_button = TextButton(Gap(), "Options")
        self.restart_button = TextButton(Gap(), "Restart")
        self.quit_button = TextButton(Gap(), "Quit")
        super().__init__(*self.__dict__.values())


class EndGameMenu(pygame.sprite.Group):

    def __init__(self, screen_size:tuple, *args, **kwargs):
        WIDTH, HEIGHT = screen_size
        font_size = 32
        Gap = MenuCentered(screen_size, font_size, 2)
        self.quit_button = TextButton(Gap(), "Close")
        self.new_game_button = TextButton(Gap(), "Play Again?")


class MenuCentered:
    """
    Generator class that provides x and why
    """
    def __init__(self, screen_size: tuple, gap_size, item_count:int):
        self.item_count = item_count
        self.WIDTH, self.HEIGHT = screen_size
        self.gap_size = gap_size
        self.current = 0

    def __call__(self):
        return next(self)

    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < self.item_count:
            x = self.WIDTH // 2
            y = (self.HEIGHT // 2) + (self.gap_size * self.current)
            print(self.current)
            self.current += 1
            return x,y
        raise StopIteration
