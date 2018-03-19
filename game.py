from classyDungeon import Dungeon
import pygame

class Game():
    def __init__(self, screen_size):
        # TODO make this more dynamic
        self.SIZE = screen_size
        self.WIDTH, self.HEIGHT = screen_size
        self.TILESIZE = 32
        self.GRIDWIDTH = self.WIDTH // self.TILESIZE
        self.GRIDHEIGHT = self.HEIGHT // self.TILESIZE
        self.dungeon = Dungeon(resolution=(self.GRIDWIDTH,self.GRIDHEIGHT), roomCount=5)
        self.dungeon.make()
        pygame.init()
        self.display = pygame.display.set_mode(self.SIZE)
        self.game_over = False

    def setup(self):
        pygame.display.set_caption('Dungoen')

    def game_loop(self):
        while not self.game_over:
            self.draw()
            self.events()

    def draw(self):
        self.dungeon.draw(self)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()
            print(event)

    def end(self):
        pygame.quit()
        quit()

if __name__ == '__main__':
    newgame = Game((600,800))
    newgame.setup()
    newgame.game_loop()
