import random

import Setup
from Setup import *
from datetime import datetime, timedelta


class Dust:
    dust_gif = Image.open("Assets/player/DUSTCLOUD.gif")
    dust_frames = []
    for i in range(dust_gif.n_frames):
        dust_frames.append(pil_to_game(get_gif_frame(dust_gif, i)))

    def __init__(self, pos, dust_size, direction):
        self.position = pg.Vector2(pos)
        self.dust_size = dust_size
        self.velocity = pg.Vector2(0,0)
        self.direction = -direction
        self.current_frame = 0
        self.display = self.dust_frames[math.floor(self.current_frame)]
        Setup.particles.append(self)

    def update(self, delta):
        self.position += self.velocity
        self.velocity = pg.Vector2(self.direction * delta / 64, -self.current_frame * delta / 256)
        self.display = pg.transform.scale(self.dust_frames[math.floor(self.current_frame)], (self.dust_size, self.dust_size))
        self.current_frame = (self.current_frame + 0.25)
        if math.floor(self.current_frame) >= self.dust_gif.n_frames-1:
            del Setup.particles[Setup.particles.index(self)]

    def draw(self, surf):
        surf.blit(self.display, get_display_point(self.position))

class Cloud:
    img = pg.image.load("Assets/world/CLOUD.png")

    def __init__(self, pos, cloud_size):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(random.random()/5000,0)
        self.cloud_size = cloud_size
        self.display_img = pg.transform.scale(self.img, (self.cloud_size, self.cloud_size))
        Setup.particles.append(self)

    def update(self, delta):
        self.position += self.velocity * delta

    def draw(self, surf):
        surf.blit(self.display_img, self.position - Setup.camera_offset * 0.25)

class Treasure:
    imgs = [pg.image.load("Assets/world/decor/GOLDCOIN.png"),
            pg.image.load("Assets/world/decor/SILVERCOIN.png"),
            pg.image.load("Assets/world/decor/BRONZECOIN.png"),
            pg.image.load("Assets/world/decor/JEWEL.png"),
            ]
    for i, val in enumerate(imgs):
        imgs[i] = pg.transform.scale(val, (50, 50))
    width, height = imgs[0].get_size()
    gravity = 0.098
    friction = 0.9

    def __init__(self, pos,vel, collision_layer, collision_mask):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(vel)
        collision_layer.add(self)
        self.collision_mask = collision_mask
        self.display = random.choice(self.imgs)
        self.attacked = False
        self.health = 1000
        self.invincibility_frames = 250
        self.on_ground = False

        self.set_pos = False

    def update(self, delta, pos):
        if not self.set_pos:
            self.position = pg.Vector2(pos)
            self.set_pos = True

        if self.on_ground:
            self.velocity.x *= self.friction
        self.velocity.y += self.gravity

        self.position, self.velocity = self.move_and_collide(self.position, self.velocity,delta)
    def attack(self, enemy, weapon, direction):
        if not self.attacked and self.invincibility_frames == 0:
            self.push(direction, 3, -5)
            self.attacked = True
            self.invincibility_frames = 250
    def push(self, direction, strength=1, y=-1):
        self.velocity += pg.Vector2(direction * strength, y)
    def move_and_collide(self, pos, vel, delta):
        pos.x += vel.x * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:
            for thing in mask:
                if thing == self:
                    continue
                if collision_rect.colliderect(thing.get_collision_rect()):
                    # print(self, self.position.x, self.velocity.x)
                    # if thing.movable:
                    #     if vel.x > 0:
                    #         thing.position.x = pos.x + self.width
                    #     elif vel.x < 0:
                    #         thing.position.x = pos.x - thing.width
                    if vel.x > 0:
                        pos.x = thing.position.x - self.width
                        vel.x = min(vel.x, 0)
                    elif vel.x < 0:
                        pos.x = thing.position.x + thing.width
                        vel.x = max(vel.x, 0)
                        # print(pos.x, vel.x)
                    collision_rect = self.get_collision_rect(pos)

        self.on_ground = False
        pos.y += vel.y * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:
            for thing in mask:
                if thing == self:
                    continue
                if collision_rect.colliderect(thing.get_collision_rect()):
                    if vel.y >= 0:
                        pos.y = thing.position.y - self.height
                        vel.y = min(vel.y, 0)
                        self.on_ground = True
                    elif vel.y < 0:
                        pos.y = thing.position.y + thing.height
                        vel.y = max(vel.y, 0)
                    collision_rect = self.get_collision_rect(pos)
        return pos, vel

    def get_collision_rect(self, pos=None):
        if pos is None:
            pos = self.position
        return pg.Rect(pos, (self.width, self.height))

    def draw(self, surf):
        surf.blit(self.display, get_display_rect(self.get_collision_rect()))
