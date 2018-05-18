
'''
Animations Each row has 10 animations

1: Idle 1-10
2: Emote 11-20
3: Walk 21-30
4: Attack 31-40
5: Death 41-50
''' 

from os import path
import pygame
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
song_direc = package_path + "\music"
db = package_path + "\data"
if 'home' in package_path:
    img_direc = package_path + "/img"
    song_direc = package_path + "/music"
    db = package_path + "/data"


errors = 0
try:
    tiles = pygame.image.load(path.join(img_direc ,"dungeon_floor.png"))
    rouge = pygame.image.load(path.join(img_direc, "rouge.png"))
    skeleton = pygame.image.load(path.join(img_direc,"skeleton.png"))
    door = pygame.image.load(path.join(img_direc, "Doors.jpg"))
except TypeError:
    tiles = pygame.image.load(img_direc + "dungeon_floor.png")
    rouge = pygame.image.load(img_direc + "rouge.png")
    skeleton = pygame.image.load(img_direc + "skeleton.png")
    door = pygame.image.load(img_direc + "Doors.jpg")


FileDoc = namedtuple('FileDoc', ['Reference', 'Picture'])

# Range not implemented yet
Sheets = {"Tile": FileDoc(Tiles_and_ceil_ref, tiles),
          "Door": FileDoc(doors_ref, door),
          "Rouge":FileDoc(rouge_ref, rouge),
          "Player":FileDoc(rouge_ref, rouge),
          "Monster": FileDoc(skeleton_ref,skeleton),
          "Skeleton": FileDoc(skeleton_ref,skeleton),
          "BossSkeleton": FileDoc(skeleton_ref,skeleton)}
           # The first one is the name of the image Dict, The second to the name of the file

all_sprites = pygame.sprite.Group()

def get_img(key_name, sprite_number):
    ref = Sheets[key_name].Reference[sprite_number]
    img = pygame.Surface((ref[2], ref[3]))
    img.blit(Sheets[key_name].Picture, (0,0),ref)
    return img

def get_all_images(class_name: str) -> dict:
    """ Runs get image for a whole person"""
    image_dict = {}
    for i in range(0,4):
        surface_list = []
        for j in range(1,11):
            surface_list.append(get_img(class_name,(i*10)+j))
        image_dict[transform(i)] = surface_list

    return image_dict
    
def transform(thing:int):
    if thing == 0: return 'Idle'
    if thing == 1: return 'Emote'
    if thing == 2: return 'Walk'
    if thing == 3: return 'Attack'
    if thing == 4: return 'Death'

class Camera():
    """
    This allows for simple parallax scrolling
    """
    def __init__(self, width, height):
        self.Camera = pygame.Rect(0, 0, width, height)
        self.width, self.height = width, heigh
    
