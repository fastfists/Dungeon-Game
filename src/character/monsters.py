"""More structered implementation
of my sprites
"""
import random
import json
from os import path

from . import utils, artifacts, Monster, DungeonElement

class Skeleton(Monster):
    default_state = 'Walk'
    possible_states = {'Walk', 'Attack'}
    animation_speed = 0.88
    speed = 0.03
    flip = False

    def __init__(self, *args, **kwargs):
        self.direction = random.choice(['West', 'East'])
        super().__init__(*args, **kwargs)

    def draw(self, *args, **kwargs):
        super().draw(*args, flip=self.flip, **kwargs)

    @property
    def x_limit(self):
        return self.room.blocks[0].x, self.room.blocks[-1].x

    @property
    def y_limit(self):
        return self.room.blocks[0].y, self.room.blocks[-1].y

    def update(self, active: bool):
        if not self.dead:
            super().update()
            if active:
                self.state = "Walk"
                if self.x >= self.x_limit[1]:
                    self.direction = 'West'
                elif self.x <= self.x_limit[0]:
                    self.direction = 'East'

                if self.direction == 'East':
                    self.x += self.speed
                    self.flip = False
                elif self.direction == 'West':
                    self.x -= self.speed
                    self.flip = True

                choice = random.choice([self.speed, -self.speed])
                self.y += choice
                if self.y < self.y_limit[0] or self.y > self.y_limit[1]:
                    # if out of bounds
                    self.y -= choice

            else:
                self.state = "Idle"


class BossSkeleton(Skeleton, picture_name="Skeleton"):
    health = 200
    def __init__(self, *args, level=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_skeletons = self.levels(level)
        self.size *= 8
        self.size //= 2
        self.skelton_spawner = artifacts.Emitter(Skeleton, lambda skel: skel.state != 'Dead',
                                                 cooldown=50, element_args=[self.room])
        

    @staticmethod
    def levels(level: int) -> int:
        """ Method that returns the limit of skeletons to spawn based on level """
        with open(path.join(utils.db,"Characters", "boss_skeleton.json")) as f:
            data = json.load(f)
            return data[f"Level {level}"]

    def draw(self, *args, **kwargs):
        super().draw()

    def spawn_skeleton(self):
        if self.skelton_spawner.ready:
            self.state = "Attacking"
            x, y = self.position
            start_pos = x + random.uniform(.5, .10), y + random.uniform(.5, .10)
            self.skelton_spawner.load(additional_kwargs={'position': start_pos})
            self.dungeon.elements.add(self.skelton_spawner[-1])
            self.room.monsters.append(self.skelton_spawner[-1])

    def update(self, active):
        super().update(active)
        if active and not self.dead:
            if len(self.skelton_spawner) != self.max_skeletons:
                self.spawn_skeleton()
        self.skelton_spawner.update(active)


class Goblin(Monster):
    
    def __init__(self, room, position=None):
        speed = 0.7