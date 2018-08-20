from . import TextButton
import pygame


def say_hello():
    print("Hello")

class PauseMenu(pygame.sprite.Group):
    font_size = 32

    def __init__(self, screen_size:tuple, *a, **kw):
        WIDTH, HEIGHT = screen_size
        self.resume_button = TextButton((WIDTH / 2, (HEIGHT / 2) - self.font_size*2), "Resume")
        self.options_button = TextButton((WIDTH / 2, (HEIGHT / 2) - self.font_size ), "Options")
        self.restart_button = TextButton((WIDTH / 2, (HEIGHT / 2) + self.font_size ), "Restart")
        self.quit_button = TextButton((WIDTH / 2, (HEIGHT / 2) + self.font_size*2), "Quit")
        super().__init__(self.resume_button, self.options_button, self.restart_button, self.quit_button, *a, **kw)


class EndGameMenu(pygame.sprite.Group):

    def __init__(self, screen_size:tuple, *a, **kw):
        WIDTH, HEIGHT = screen_size
        self.play_again_button = TextButton((WIDTH / 2, (HEIGHT / 2) - font_size*2), "Play Again?")
        self.quit_button = TextButton((WIDTH / 2, (HEIGHT / 2) + font_size*2), "Quit")