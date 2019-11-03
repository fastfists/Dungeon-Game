from . import Sprite, DungeonElement, collides_with, utils, artifacts, pygame, Skeleton, Monster, Wall
from src.object_list import ObjectList

class Player(Sprite, DungeonElement, picture_name="Rouge"):
    animation_speed = 0.5
    speed = 0.2
    x: float
    y: float
    flip = False

    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.position = dungeon.start_pos
        Sprite.__init__(self)
        DungeonElement.__init__(self, self.position, self.dungeon)
        self.size *= 4
        self.size //= 5
        laser_dict = dict(master=self, image=pygame.transform.rotate(utils.get_img("laser_blast", 1), 90), damage=5, speed=self.speed * 3)
        sword_dict = dict(master=self, image=utils.get_single_img('sword_slash'), speed=self.speed * 3, delay=30)
        self.shooter = ObjectList([artifacts.Emitter(artifacts.Projectile, artifacts.Projectile.end_if,
                element_kwargs=sword_dict, cooldown=20),artifacts.Emitter(artifacts.Projectile, artifacts.Projectile.end_if, element_kwargs=laser_dict, cooldown=2)])

    def update(self):
        self.get_keys()
        self.shooter.update()

    def draw(self, *args, **kwargs):
        if not self.dead:
            super().animate()
            self.image.set_colorkey(utils.BLACK)
            self.shooter.emit()
            super().draw(*args, flip=self.flip, **kwargs)
            self.health.draw_bar(self.display, self.rect)

    def speed_up(self):
        self.animation_speed += 0.01
        self.speed += 0.05
        self.shooter.frame_limit -= 0.05

    def get_keys(self):
        key = pygame.key.get_pressed()
        #########################
        #  Moving of character  #
        #########################
        move_x, move_y = 0, 0
        if key[pygame.K_DOWN]:
            move_y = self.speed
        if key[pygame.K_UP]:
            move_y = -self.speed
        if key[pygame.K_LEFT]:
            move_x = -self.speed
        if key[pygame.K_RIGHT]:
            move_x = self.speed

        if key[pygame.K_s]:
            move_y = self.speed
        if key[pygame.K_w]:
            move_y = -self.speed
        if key[pygame.K_a]:
            move_x = -self.speed
        if key[pygame.K_d]:
            move_x = self.speed
        if move_x and move_y:
            move_x /= 1.41
            move_y /= 1.41
        self.x += move_x
        self.y += move_y
        if self.dungeon.Idtbl[round(self.x)][round(self.y)] == 1:
            self.x -= move_x
            self.y -= move_y

        if move_x != 0 or move_y != 0:
            self.state = 'Walk'
        else:
            self.state = 'Idle'
        if move_x < 0:
            self.flip = True
        elif move_x > 0:
            self.flip = False

        #########################
        #      Get actions      #
        #########################
        direction = (-1, 0) if self.flip else (1, 0)
        if key[pygame.K_SPACE] and self.shooter.ready[0]:
            self.state = 'Attacking'
            #self.speed_up()
            self.shooter.load(additional_kwargs=dict(start_pos=self.position, direction=direction))

        with collides_with(self, class_name=Monster) as monsters:
            for monster in monsters:
                if monster.state != "Dying":
                    self.damage(5)
