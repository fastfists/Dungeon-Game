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

        # Pause Menu
        pause_button_names = dict(resume_button="Resume", restart_button="Restart",
                            options_button="Options", quit_button="Quit")
        self.pause_menu = UI.menus.Menu((self.SIZE), pause_button_names)
        self.pause_menu.resume_button.add_action(self.toggle_pause)
        self.pause_menu.restart_button.add_action(restart)
        self.pause_menu.quit_button.add_action(true_end)

        # End Menu
        end_button_names = dict(restart_button="Try Again?", quit_button="Quit")
        self.endgame_menu = UI.menus.Menu((self.SIZE), end_button_names)
        self.endgame_menu.quit_button.add_action(true_end)
        self.endgame_menu.restart_button.add_action(restart)

    def setup(self):
        start = time.time()
        self.dungeon.make()
        end = time.time()
        print(f"Rendered Dungeon in {end - start} seconds")
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
        while True:
            self.draw()
            self.update()
            self.events()
            self.clock.tick(60)    

    def draw(self): 
        self.display.fill(BLACK, rect=None, special_flags=0)
        self.dungeon._draw()
        if self.game_over:
            self.endgame_menu.draw(self.display)
        elif self.paused:
            self.pause_menu.draw(self.display)
            for room in self.dungeon.allrooms:
                room.draw()
        
        player_state = self.dungeon.player.state
        if player_state == "Dying" or player_state == "Dead":
            send_message("U Ded noob", self.display)
            self.game_over = True


    def update(self):
        pygame.display.update()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        self.game_over = self.dungeon.is_cleared or self.game_over
        if self.game_over:
            self.endgame_menu.update(mouse_clicked)
        elif self.paused:
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
    print("ending")
    pygame.quit()
    quit()

def run():
    global game
    game = Game((1366, 768), tilesize=64)
    game.start()
    
if __name__ == '__main__':
    run()
