""" Contains the Game class"""

import random
import time

import pygame

from .utils import *

from . import UI
from . import classydungeon as dun


'''
Need to implement:
    Chests/ reward system
'''


class Game:

    def __init__(self, screen_size: tuple, tilesize=16):
        # Set Constants
        self.SIZE = screen_size
        self.WIDTH, self.HEIGHT = self.SIZE
        self.TILESIZE = tilesize
        self.GRIDWIDTH = self.WIDTH // self.TILESIZE
        self.GRIDHEIGHT = self.HEIGHT // self.TILESIZE
        # Set Up Pygame
        pygame.init()
        pygame.mixer.music.load(path.join(song_direc, 'skeletons.mp3'))

        self.paused = False

        self.clock = pygame.time.Clock()
        # Set game variables
        self.game_over = False
        # Set Up Dungeon
        try:
            self.display = pygame.display.set_mode(self.SIZE)  # TODO add full screen
        except pygame.error:
            self.display = pygame.display.set_mode(self.SIZE)
        random.seed()
        self.dungeon = dun.Dungeon.from_json(db + "/Dungeon.json", self)
        random.seed(self.dungeon.seed)

        button_names = dict(resume_button="Resume", restart_button="Restart",
                            options_button="Options", quit_button="Quit")
        self.pause_menu = UI.menus.Menu((self.SIZE), button_names)
        self.pause_menu.quit_button.add_action(self.end)
        self.pause_menu.resume_button.add_action(self.toggle_pause)
        self.pause_menu.restart_button.add_action(restart)

    def setup(self):
        start = time.time()
        self.dungeon.make()
        end = time.time()
        print(end - start)
        pygame.display.set_caption('Dungeon')
        pygame.mixer.music.play()

    def toggle_pause(self):
        """
        Toggles pasue
        """
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def start(self):
        self.setup()
        while not self.game_over:
            self.draw()
            self.update()
            self.events()
            self.clock.tick(60)

    def draw(self): 
        self.display.fill(BLACK, rect=None, special_flags=0)
        self.dungeon._draw()
        if self.paused:
            self.pause_menu.draw(self.display)
            for room in self.dungeon.allrooms:
                room.draw()
        
        state = self.dungeon.player.state
        if state == "Dying" or state == "Dead":
            send_message("U Ded noob", self.display)


    def update(self):
        pygame.display.update()
        if self.paused:
            mouse_clicked = pygame.mouse.get_pressed()[0]
            self.pause_menu.update(mouse_clicked)
        else:
            for room in self.dungeon.allrooms:
                room.update()
            self.dungeon.update_sprites()

    def events(self):
        """ The event handler for the Game object """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause()
                if event.key == pygame.K_CAPSLOCK:
                    print(self.dungeon.seed)
                    self.end()
                if event.key == pygame.K_ESCAPE:
                    self.end()

    def end(self):
        self.game_over = True

def restart():
    game.game_over = True
    new_game = Game((1366, 768), tilesize=64)
    new_game.start()

def true_end():
    pygame.quit()
    quit()

def run():
    global game
    game = Game((1366, 768), tilesize=64)
    game.start()
    
if __name__ == '__main__':
    run()
