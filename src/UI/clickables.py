from . import utils
import pygame
import numpy as np

class Clickable(pygame.sprite.Sprite):

    def __init__(self, pos:tuple, size:tuple, *actions_on_click):
        pygame.sprite.Sprite.__init__(self)
        pos, size = np.array(pos), np.array(size)
        self.rect = pygame.Rect(pos - (size / 2), size)
        self.actions = list(actions_on_click)
        self.pressed = False

    def update(self, mouse_clicked: bool):
        mouse_pos = pygame.mouse.get_pos()
        self.pressed = False
        if self.rect.collidepoint(mouse_pos):
            if not mouse_clicked:
                self.on_hover()
            else:
                self.pressed = True
                self._perform()
        else:
            self.off_hover()

    def add_action(self, action) -> None:
        self.actions.append(action)
    
    def on_hover(self):
        pass
    
    def off_hover(self):
        pass

    def _perform(self):
        for action in self.actions:
            action()
    
    def __repr__(self):
        return f"{self.__class__.__name__} object at ({self.rect.x}, {self.rect.y}) pressed {self.pressed}"
    

class TextButton(Clickable):

    def __init__(self, pos:tuple, message:str, font=utils.bold_font, *actions_on_click):
        self.message = message
        self.color = utils.WHITE
        self.font = font
        self.text = self.font.render(self.message, True, self.color)
        size = self.text.get_rect().size
        super().__init__(pos, size, *actions_on_click)

    @property
    def image(self):
        return self.text

    @image.setter
    def image(self, new_image):
        self.text = new_image

    def update(self, mouse_clicked):
        self.text = self.font.render(self.message, True, self.color)
        super().update(mouse_clicked)
    
    def on_hover(self):
        self.color = utils.GREEN

    def off_hover(self):
        self.color = utils.WHITE
