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
        try: self.display = pygame.display.set_mode(self.SIZE,pygame.FULLSCREEN)
        except pygame.error: self.display = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()
        # Set game variables
        self.game_over = False
        # Set Up Dungeon
        self.dungeon = dun.Dungeon(resolution=(self.GRIDWIDTH,self.GRIDHEIGHT), roomCount=20, game = self)


    def set_sizes(self, size):
        dun.Tile.tile_size = size
        dun.Wall.wall_size = size


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
        self.display.fill(BLACK, rect=None, special_flags=0)
        self.dungeon._draw()
        self.player.show()
        for room in self.dungeon.allrooms:
            room.activate()

    def update(self):
            pygame.display.update()
            self.player.update()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()
            if event.type == pygame.KEYDOWN:
                x,y = 0, 0
                if event.key == pygame.K_DOWN:  y += 1
                if event.key == pygame.K_UP:    y -= 1
                if event.key == pygame.K_LEFT:  x -= 1
                if event.key == pygame.K_RIGHT: x += 1
                
                self.player.move(xChange=x, yChange=y)
                
                if event.key == pygame.K_ESCAPE:
                    self.end()
        


    def end(self):
        pygame.quit()
        quit()


if __name__ == '__main__':
    newgame = Game((1080, 920), tilesize=32)
    newgame.run()
