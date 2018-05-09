''' Contains the Game class'''


from utils import *
import pygame
import characters
import classydungeon as dun 


'''
Whats broken:
    Need better tiles (make them?)

Need to implement:
    sprite dictionary state
    Sprite interactions
    Chests/ reward system
'''

class Game():
    
    def __init__(self, screen_size:tuple, tilesize=16):
        # Set Constants
        self.SIZE = screen_size
        self.WIDTH, self.HEIGHT = self.SIZE
        self.TILESIZE = tilesize
        self.GRIDWIDTH = self.WIDTH // self.TILESIZE
        self.GRIDHEIGHT = self.HEIGHT // self.TILESIZE
        # Set Up Pygame
        pygame.init()
        pygame.mixer.music.load(song_direc + '/skeletons.mp3')


        self.clock = pygame.time.Clock()
        # Set game variables
        self.game_over = False
        # Set Up Dungeon
        try: self.display = pygame.display.set_mode(self.SIZE) # TODO add fullscreen
        except pygame.error: self.display = pygame.display.set_mode(self.SIZE)
        self.dungeon = dun.Dungeon((self.GRIDWIDTH, self.GRIDHEIGHT), 10, self, seed=54545)

    def setup(self):
        self.dungeon.make()
        pygame.display.set_caption('Dungoen')
        self.player = characters.Player(self.dungeon.start_pos, self)
        pygame.mixer.music.play()

    def __enter__(self):
        self.setup()
        while not self.game_over:
            self.draw()
            self.update()
            self.events()
            self.clock.tick(60)

    def draw(self):
        self.display.fill(GRAY, rect=None, special_flags=0)
        self.dungeon._draw()

        #self.dungeon._draw(tilesize=10) # draws the mini map

        self.player.show()
        for room in self.dungeon.allrooms:
            room.activate()

    def update(self):
            pygame.display.update()
            self.player.update()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit__()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_CAPSLOCK:
                    print(self.dungeon.seed)
                    self.__exit__()
                if event.key == pygame.K_ESCAPE:
                    self.__exit__()
        


    def __exit__(self):
        pygame.quit()
        quit()


if __name__ == '__main__':
    game = Game((1366,768), tilesize=64)
    with game:
        import pprint; pprint.pprint(game.dungeon.elements)
        print("We Made It")
