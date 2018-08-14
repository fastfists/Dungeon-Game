from . import TextButton
import pygame


def say_hello():
    print("Hello")

class PauseMenu(pygame.sprite.Group):

    def __init__(self, screen_size:tuple, *args, **kwargs):
        WIDTH, HEIGHT = screen_size
        font_size = 32
        self.resume_button = TextButton((WIDTH / 2, (HEIGHT / 2) - font_size*2), "Resume")
        self.options_button = TextButton((WIDTH / 2, (HEIGHT / 2) - font_size ), "Options")
        self.restart_button = TextButton((WIDTH / 2, (HEIGHT / 2) + font_size ), "Restart")
        self.quit_button = TextButton((WIDTH / 2, (HEIGHT / 2) + font_size*2), "Quit")
        super().__init__(*self.__dict__.values())