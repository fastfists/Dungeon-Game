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
img_direc = path.join(package_path, "img")
song_direc = path.join(package_path, "music")
db = path.join(package_path, "data")

FileDoc = namedtuple('FileDoc', ['Reference', 'Picture'])
sprite_sheet_names =["Tile.png", "Rouge.png", "Skeleton.png", "Door.jpg", "sword_slash.jpg", "Ranger.png"]
sheets = {}
for name in sprite_sheet_names:
    name, ext = name.split('.')
    exec(f"{name} = pygame.image.load(path.join(img_direc ,'{name +'.' +ext}'))")
    exec(f"sheets[name] = FileDoc({name}_ref, {name})")




all_sprites = pygame.sprite.Group()
def get_single_img(name):
    if name in sheets.keys():
        return sheets[name].Picture

def get_img(key_name, sprite_number):
    if name in sheets.keys():
        ref = sheets[key_name].Reference[sprite_number]
        img = pygame.Surface((ref[2], ref[3]))
        img.blit(sheets[key_name].Picture, (0,0),ref)
        return img

def get_all_images(class_name: str) -> dict:
    """ Runs get image for a whole person"""
    image_dict = {}
    for i in range(0,5):
        surface_list = []
        for j in range(1,11):
            surface_list.append(get_img(class_name,(i*10)+j))
        image_dict[transform(i)] = surface_list
    return image_dict

def transform(thing:int):
    if thing == 0: return 'Idle'
    if thing == 1: return 'Emote'
    if thing == 2: return 'Walk'
    if thing == 3: return 'Attacking'
    if thing == 4: return 'Dying'

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

@parametrized
def collides_with(func, sprite_1, sprite_group):
    """ function wrapper of that determines if two sprites collide
        Should recieve a sprite and as sprite group 
    """
    def wrapper(*args, **kwargs):
        collided =  pygame.sprite.spritecollide(sprite_1, sprite_group, False, collided = None)
        if pygame.sprite.spritecollide(sprite_1, sprite_group, False, collided = None):
            return func(*args, **kwargs, hit = collided)
    return wrapper

def send_messgage():
    pass