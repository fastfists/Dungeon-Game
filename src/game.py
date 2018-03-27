''' Contains the Game class'''


from utils import *
import pygame
import characters
import classydungeon as dun 


'''
Whats broken:
    Walls look funky
    Need better tiles (make them?)
    Sprite animation / States(for player class)

Need to implement:
    Sprite interactions
    Chests/ reward system
'''

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
        try: self.display = pygame.display.set_mode(self.SIZE, pygame.FULLSCREEN)
        except pygame.error: self.display = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()
        # Set game variables
        self.game_over = False
        # Set Up Dungeon
        self.dungeon = dun.Dungeon(resolution=(self.GRIDWIDTH,self.GRIDHEIGHT), roomCount=5, game = self)

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
        self.display.fill(GRAY, rect=None, special_flags=0)
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

                
                if event.key == pygame.K_ESCAPE:
                    self.end()
        


    def end(self):
        pygame.quit()
        quit()


def test(type):
    if type == "tk":
        try:    
            from tkinter import Tk, Canvas
            from pprint import pprint
            newgame = Game((1920, 1080), tilesize=64)
            pygame.quit()
            newgame.dungeon.make()
            master = Tk()
            boi = Canvas(master,width=newgame.WIDTH,height=newgame.HEIGHT)
            for y in range(newgame.dungeon.HEIGHT):
                for x in range(newgame.dungeon.WIDTH):
                    w = 1
                    o = 'black'
                    ide = newgame.dungeon.Idtbl[x][y]
                    if ide == 0:
                        f = 'gray'
                    elif ide == 1:
                        f = 'black'
                    elif ide == 2:
                        f = 'blue'
                    elif ide == 3:
                        f = 'green'
                    elif ide == 4:
                        f = 'purple'
                    elif ide == 5:
                        f = 'yellow'
                    elif ide == (4,2):
                        f = 'brown'
                    elif ide == -1:
                        f = 'orange'
                    boi.create_rectangle(
                                            x*(700//newgame.dungeon.WIDTH),
                                            (y*(700//newgame.dungeon.HEIGHT)),
                                            (x+1)*(700//newgame.dungeon.WIDTH)-1,
                                            (y+1)*(700//newgame.dungeon.HEIGHT)-1,
                                            fill=f,
                                            outline=o,
                                            width=w
                                        )
                    boi.pack()
            master.mainloop()
        except KeyboardInterrupt:
            print(negame.dungeon.seed) 
    else:
        
        newgame = Game((1366,768), tilesize=64)
        newgame.run()


if __name__ == '__main__':
    test("tdk")
    
