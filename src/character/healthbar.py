import pygame
from . import utils

class HealthBar:
    
    def __init__(self, current_health, max_health, width):
        self.max_health = max_health
        self.height, self.width  = 5, width
        self.current_health = current_health
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(utils.GRAY)
        self.render_health_bar()

    def render_health_bar(self):
        # blit health indicator to empty box
        self.update()
        self.health_bar = pygame.Surface((self.width, self.height))
        self.health_bar.blit(self.foreground, (0,0))

    def update(self):
        # Create a new health indicator
        health_length = (self.current_health * self.width) // self.max_health
        health_length = health_length if health_length >= 0 else 0        
        self.foreground = pygame.Surface((health_length,self.height))
        self.foreground.fill(utils.GREEN)

    def draw_bar(self, screen: pygame.surface.Surface, target_rect:pygame.Rect):
        position = target_rect.x, target_rect.y - self.height
        screen.blit(self.health_bar, position)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        try:
            self._width = width
            self.render_health_bar()
        except:
            pass
    @property
    def current_health(self):
        return self._current_health

    @current_health.setter
    def current_health(self, value):
        if value > self.max_health:
            value = self.max_health
        self._current_health = value
        ## create a new health bar
        self.render_health_bar()

    def __eq__(self, other):
        return int(self) == int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __le__(self, other):
        return int(self) <= int(other)
        
    def __int__(self):
        return self.current_health

    def __add__(self, other):
        new_health = int(self) + int(other)
        return HealthBar(new_health, self.max_health, self.width)

    def __iadd__(self, value):
        self.current_health += int(value)
        return self

    def __isub__(self, value):
        self.current_health -= int(value)
        return self
    