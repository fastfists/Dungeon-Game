from classydungeon import *
from characters import *
#import pygame


class Game():
    def __init__(self, size):
        # TODO make this more dynamic
        self.WIDTH, self.HEIGHT = size
        self.dungeon = Dungeon(resolution=(self.WIDTH//10,self.HEIGHT//10), roomCount=5)
        self.dungeon.make()
        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game_over = False

    def setup(self):
        pygame.display.set_caption('Dungoen')

    def game_loop(self):
        while not self.game_over:
            self.events()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()
            print(event)

    def end(self):
        pygame.quit()
        quit()

if __name__ == '__main__':
    newgame = Game((600,400))
    newgame.setup()
    newgame.game_loop()
