"""
Animations Each row has 10 animations

1: Idle 1-10
2: Emote 11-20
3: Walk 21-30
4: Attack 31-40
5: Death 41-50
"""
import functools
from collections import namedtuple
from os import path
import pygame
from .maps import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
PURPLE = (145, 57, 92)
ORANGE = (255, 98, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

package_path = path.dirname(path.dirname(__file__))
img_direc = path.join(package_path, "img")
song_direc = path.join(package_path, "music")
db = path.join(package_path, "data")

FileDoc = namedtuple('FileDoc', ['Reference', 'Picture'])
sprite_sheet_names = ["Tile.png", "Rouge.png", "Skeleton.png", "Door.jpg", "sword_slash.jpg",
                      "Ranger.png","sci_fi.png", "Goblin.png", "robot_mouthopen.png",
                      "robot_mouthclosed.png", "Containers.png","Potions.png", "laser_blast.png"]
sheets = {}
for name in sprite_sheet_names:
    name, ext = name.split('.')
    exec(f"{name} = pygame.image.load(path.join(img_direc ,'{name +'.' +ext}'))")
    exec(f"sheets[name] = FileDoc({name}_ref, {name})")

robot_mouthclosed = pygame.transform.scale(robot_mouthclosed, (180, 100))
robot_mouthopen = pygame.transform.scale(robot_mouthopen, (180, 100))

dialouge_box: pygame.surface.Surface = pygame.image.load(path.join(img_direc, "Dialouge_box.png"))
pygame.font.init()

robot_font = pygame.font.Font(path.join(db, "Fonts", "HUMANOID.TTF"), 32)
bold_font = pygame.font.Font(path.join(db, "Fonts", "Under_the_Weather.otf"), 50)

def get_single_img(name):
    if name in sheets.keys():
        return sheets[name].Picture


def get_img(key_name, sprite_number) -> pygame.Surface:
    if name in sheets.keys():
        ref = sheets[key_name].Reference[sprite_number]
        img = pygame.Surface((ref[2], ref[3]))
        img.blit(sheets[key_name].Picture, (0, 0), ref)
        return img


def get_all_images(class_name: str) -> dict:
    """ Runs get image for a whole person"""
    image_dict = {}
    for i in range(0, 5):
        surface_list = []
        for j in range(1, 11):
            surface_list.append(get_img(class_name, (i * 10) + j))
        image_dict[transform(i)] = surface_list
    return image_dict


def transform(thing: int):
    if thing == 0: return 'Idle'
    if thing == 1: return 'Emote'
    if thing == 2: return 'Walk'
    if thing == 3: return 'Attacking'
    if thing == 4: return 'Dying'

def do_once(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        try:
            if not func.called:
                func(*a, **kw)
                func.called = True
        except AttributeError:
            func(*a, **kw)
            func.called = True
    return wrapper

class Ignore:
    pass


robot = 0
bot = None

def change_bot(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        global robot, bot
        if robot % 5 == 0:
            if bot is robot_mouthclosed:
                bot = robot_mouthopen
            else:
                bot = robot_mouthclosed
        robot += 1
        return func(*args, bot, **kwargs)
    return wrapped


@change_bot
def send_message(msg, screen, bot: Ignore):
    box = dialouge_box

    screen_text = robot_font.render(msg, True, PURPLE)
    box.blit(screen_text, (240, 40))
    box.blit(bot, (0, 0))

    box = pygame.transform.scale(box, (int(screen.get_width() * .60) ,int(screen.get_height() * .20)))

    box.set_alpha(190)
    screen.blit(box, (int((screen.get_width() - box.get_width()) // 2),
                      int((screen.get_height() - box.get_height()) *0.80)))
