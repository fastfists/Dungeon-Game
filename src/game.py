''' Contains the Game class'''


from utils import *
import pygame
import characters
import classydungeon as dun 




class Game():

    def __init__(self, screen_size:tuple, tilesize=16):
        # Set Constants
        self.SIZE = screen_size
        self.WIDTH, self.HEIGHT = self.SIZE
        self.TILESIZE = tilesize
        self.set_sizes(tilesize)
        self.GRIDWIDTH = self.WIDTH // self.TILESIZE
        self.GRIDHEIGHT = self.HEIGHT // self.TILESIZE
        # Set Up Pygame
        pygame.init()
        self.display = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()
        # Set game variables
        self.game_over = False
        # Set Up Dungeon
        
        self.dungeon = dun.Dungeon(resolution=(self.GRIDWIDTH,self.GRIDHEIGHT), roomCount=8, game = self, seed=5)


    def set_sizes(self, size):
        
        dun.Tile.set_tile_size(size)
        dun.Wall.set_wall_size(size)

    def setup(self):
        self.dungeon.make()
        pygame.display.set_caption('Dungoen')
        self.player = characters.Player(self.dungeon.start_pos, self)
    
    def run(self):
        self.setup()
        while not self.game_over:
            self.draw()
            self.update()
            self.events()
            self.clock.tick(60)

    def draw(self):
        self.dungeon._draw()
        self.player.show
        for room in self.dungeon.allrooms:
            room.activate()

    def update(self):
        pygame.display.update()
        for x in range(self.GRIDHEIGHT):
            pygame.draw.line(self.display, (0,255,255), (0, x*self.TILESIZE), (self.HEIGHT,x*self.TILESIZE))
        for y in range(self.GRIDWIDTH):
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
    newgame = Game((1080,920), tilesize=64)
    newgame.run()
