''' Contains the Game class'''
try:
    from colors import *
except ImportError: pass
try:
    import pygame
except ImportError: pass
try:
    from classydungeon import *
except ImportError: pass
try:
    from characters import Player
except ImportError: pass
from pprint import pprint


class Game():

    def __init__(self, screen_size, tilesize=32):
        # TODO make this more dynamic
        self.clock = pygame.time.Clock()
        self.SIZE = screen_size
        self.WIDTH, self.HEIGHT = screen_size
        self.TILESIZE = tilesize
        self.GRIDWIDTH = self.WIDTH // self.TILESIZE
        self.GRIDHEIGHT = self.HEIGHT // self.TILESIZE
        self.dungeon = Dungeon(resolution=(self.GRIDWIDTH,self.GRIDHEIGHT), roomCount=14, game = self, seed=30)
        self.dungeon.make()
        pygame.init()
        self.display = pygame.display.set_mode(self.SIZE)
        self.game_over = False

    def setup(self):
        pygame.display.set_caption('Dungoen')

    def game_loop(self):
        while not self.game_over:
            self.draw()
            self.update()
            self.events()

    def draw(self):
        self.dungeon._draw()
        self.Player.show

    def update(self):
        pygame.display.update()
        for x in range(self.GRIDWIDTH):
            pygame.draw.line(self.display, (0,255,255), (0, x*self.TILESIZE), (self.HEIGHT,x*self.TILESIZE))
        for y in range(self.GRIDHEIGHT):
            pygame.draw.line(self.display, (0,255,255), (y*self.TILESIZE, 0), (y*self.TILESIZE, self.WIDTH))


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()
            print(event)

    def end(self):
        pygame.quit()
        quit()


if __name__ == '__main__':
    newgame = Game((600,800),tilesize=64)
    newgame.setup()
    newgame.game_loop()
