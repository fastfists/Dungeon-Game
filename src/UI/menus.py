from . import TextButton
import pygame


def say_hello():
    print("Hello")

class PauseMenu(pygame.sprite.Group):

    def __init__(self, screen_size:tuple, *args, **kwargs):
        WIDTH, HEIGHT = screen_size
        font_height = 31
        self.resume_button = TextButton((WIDTH / 2, (HEIGHT / 2) - font_height), "Resume")
        self.options = TextButton((WIDTH / 2, (HEIGHT / 2) ), "Options")
        self.quit_button = TextButton((WIDTH / 2, (HEIGHT / 2) + font_height), "Quit")
        super().__init__(self.resume_button, self.quit_button, self.options)