from os import path
try:
    import pygame
except ImportError: pass

from maps import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
PURPLE = (145, 57, 92)
ORANGE = (255, 98, 0)

package_path = path.dirname(path.dirname(__file__))
tile_direc = package_path + "\img" + "\dungeon_floor.png"
Tiles_and_ceil = pygame.image.load(tile_direc)

Sheets = { "Tile": (Tiles_and_ceil_ref, Tiles_and_ceil)} # The first one is the name of the image Dict, The second to the name of the file

def get_img(file_name, sprite_number):
    ref = Sheets[file_name][0][sprite_number]
    img = pygame.Surface((ref[2], ref[3]))
    img.blit(Tiles_and_ceil, (0,0),ref)
    return img


