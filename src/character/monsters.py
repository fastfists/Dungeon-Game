"""More structered implementation
of my sprites
"""
import random
import json
from os import path

from . import utils, artifacts, Monster, DungeonElement, collides_with, Wall

class Skeleton(Monster):
    default_state = 'Walk'
    possible_states = {'Walk', 'Attack'}
    animation_speed = 0.3
    speed = 0.01
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

    def on_death(self):
        super().on_death()
        self.room.power_up()
        if self.room.is_cleared:
            self.room.dungeon.power_up()

    def power_up(self):
        self.speed += 0.01

    def update(self, active: bool):
        if not self.dead:
            super().update()
            if active:
                self.state = "Walk"
                with collides_with(self, Wall) as walls:
                    if walls:
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
    health = 500
    speed = 0.02
    def __init__(self, *args, level=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_skeletons = self.levels(level)
        self.size *= 8
        self.size //= 2
        self.revenge = 0
        self.skelton_spawner = artifacts.Emitter(Skeleton, lambda skel: skel.state != 'Dead',
                                                 cooldown=50, element_args=[self.room])
        [self.spawn_skeleton() for i in range(random.randint(3,5))]

    def on_death(self):
        super().on_death()
        utils.send_message("The boss revenge begins", self.room.dungeon.game.display)
        for i in range(self.revenge % 2):
            self.room.dungeon.power_up()
            self.room.power_up()
            self.room.power_up()

    def power_up(self):
        self.speed -= 0.01


    @staticmethod
    def levels(level: int) -> int:
        """ Method that returns the limit of skeletons to spawn based on level """
        with open(path.join(utils.db,"Characters", "boss_skeleton.json")) as f:
            data = json.load(f)
            return data[f"Level {level}"]

    def spawn_skeleton(self):
        def on_skeleton_death():
            self.revenge += 1

        if self.skelton_spawner.ready:
            self.state = "Attacking"
            x, y = self.position
            start_pos = x + random.uniform(-.1, .1), y + random.uniform(-3, 3)
            self.skelton_spawner.load(additional_kwargs={'position': start_pos})
            self.dungeon.elements.add(self.skelton_spawner[-1])
            self.skelton_spawner[-1].on_death = on_skeleton_death
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
