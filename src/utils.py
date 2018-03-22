
'''
Animations Each row has 10 animations

1: Idle
2: Dancing
3: Walking
4: Attacking
5: Death
''' 

from os import path
try:
    import pygame
except ImportError as e: print(e)

from maps import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
PURPLE = (145, 57, 92)
ORANGE = (255, 98, 0)
BLACK = (0,0,0)

package_path = path.dirname(path.dirname(__file__))
img_direc = package_path + "\img"

Tiles_and_ceil = pygame.image.load(img_direc + "\dungeon_floor.png")
rouge = pygame.image.load(path.join(img_direc, "rouge.png"))
skeleton = pygame.image.load(path.join(img_direc,"skeleton.png"))

# Range not implemented yet
Sheets = { "Tile": (Tiles_and_ceil_ref, Tiles_and_ceil),
           "Rouge":(rouge_ref, rouge),
           "Skeleton": (skeleton_ref,skeleton)} # The first one is the name of the image Dict, The second to the name of the file

def get_img(key_name, sprite_number):
    ref = Sheets[key_name][0][sprite_number]
    img = pygame.Surface((ref[2], ref[3]))
    img.blit(Sheets[key_name][1], (0,0),ref)
    return img


