import pygame
from typing import List
import utils
import sys
from time import time
class Clickable(pygame.sprite.Sprite):

    def __init__(self, pos:tuple, size:tuple, *actions_on_click):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(pos, size)
        self.actions = actions_on_click

    def update(self, mouse_clicked: bool):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not mouse_clicked:
                self.on_hover()
            else:
                self._perform()
        else:
            self.off_hover()

    def on_hover(self):
        pass
    
    def off_hover(self):
        pass

    def _perform(self):
        for action in self.actions:
            action()

class TextButton(Clickable):

    def __init__(self, pos:tuple, message:str, *actions_on_click):
        self.message = message
        self.color = utils.WHITE
        self.text = utils.robot_font.render(self.message, True, self.color)
        self.image = self.text
        size = self.text.get_rect().size
        super().__init__(pos, size, *actions_on_click)

    @property
    def image(self):
        return self.text
    
    @image.setter
    def image(self, new_image):
        self.text = new_image

    def update(self, mouse_clicked):
        self.text = utils.robot_font.render(self.message, True, self.color)
        super().update(mouse_clicked)
    
    def on_hover(self):
        self.color = utils.GREEN

    def off_hover(self):
        self.color = utils.WHITE

def say_hello():
    print("Hello")

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    display = pygame.display.set_mode((600, 400), 0)
    clock = pygame.time.Clock()

    _break = False
    Hello = TextButton((300, 200), "Hello, World", say_hello)
    pause_menu = pygame.sprite.Group(Hello)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _break = True
                break

        if _break:
            break
        mouse_clicked = pygame.mouse.get_pressed()[0]        
        s = time()
        pause_menu.update(mouse_clicked)
        e = time()
        print(s - e)
        pause_menu.draw(display)
        pygame.display.update()
    pygame.quit()
    sys.exit()