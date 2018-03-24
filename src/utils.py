
'''
Animations Each row has 10 animations

1: Idle 1-10
2: alt_action 11-20
3: Walking 21-30
4: Attacking 31-40
5: Death 41-50
''' 

from os import path
try:
    import pygame
except ImportError as e: print(e)
from collections import namedtuple
from maps import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
PURPLE = (145, 57, 92)
ORANGE = (255, 98, 0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

package_path = path.dirname(path.dirname(__file__))
img_direc = package_path + "\img"

Tiles_and_ceil = pygame.image.load(img_direc + "\dungeon_floor.png")
rouge = pygame.image.load(path.join(img_direc, "rouge.png"))
skeleton = pygame.image.load(path.join(img_direc,"skeleton.png"))

FileDoc = namedtuple('FileDoc', ['Reference', 'Picture'])

# Range not implemented yet
Sheets = { "Tile": FileDoc(Tiles_and_ceil_ref, Tiles_and_ceil),
           "Rouge":FileDoc(rouge_ref, rouge),
           "Skeleton": FileDoc(skeleton_ref,skeleton)} # The first one is the name of the image Dict, The second to the name of the file

def get_img(key_name, sprite_number):
    ref = Sheets[key_name].Reference[sprite_number]
    img = pygame.Surface((ref[2], ref[3]))
    img.blit(Sheets[key_name].Picture, (0,0),ref)
    return img


