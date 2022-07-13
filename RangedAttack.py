import random

from Setup import *

class RangedAttack:
    attack_gif = Image.open("Assets/skeleton/portal.gif")
    attack_frames = []
    for i in range(attack_gif.n_frames):
        attack_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(attack_gif, i)), (480, 320)))
    def __init__(self, pos, ground, collision_layer):
        self.position = pg.Vector2(pos)
        self.timer = 0
        self.ground = ground
        self.arrows = []
        self.anim_done = False
        self.current_frame = 0
        self.display = self.attack_frames[self.current_frame]
        self.collision_layer = collision_layer

    def update(self, delta):
        self.timer += delta
        if not self.anim_done:
            self.display = self.attack_frames[math.floor(self.current_frame)]
            self.current_frame = (self.current_frame + 0.1)
            if math.floor(self.current_frame) >= self.attack_gif.n_frames - 1:
                self.anim_done = True
            if math.floor(self.current_frame) % 4 == 0 and random.random() < 0.5:
                self.arrows.append(Arrow(self.position,(random.randint(-2,2),random.random() * 2), self.ground, self.collision_layer))

        for arrow in self.arrows:
            arrow.update(delta)
    #     return True
        # return False

    def draw(self, surf):
        # pg.draw.rect(surf, (255,0,0), pg.Rect(self.position, self.display.get_size()))
        if not self.anim_done:
            surf.blit(self.display, get_display_point(self.position - pg.Vector2(self.display.get_size()) / 2))

        for arrow in self.arrows:
            arrow.draw(surf)


class Arrow:
    gravity = 0.098
    terminal_velocity = 1
    arrow = pg.transform.scale(pg.image.load("Assets/ARROW.png"), (60,60))

    def __init__(self, pos, vel, ground, collision_layer):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(vel)
        self.time = 0
        self.display = self.arrow
        self.ground = ground
        self.in_ground = False
        self.attacked = False
        self.invincibility_frames = 250
        self.timer = 6000
        collision_layer.add(self)
        self.used = False

    def attack(self, enemy, weapon, direction):
        if not self.attacked and self.invincibility_frames == 0:
            self.push(direction, 3, -4)
            self.attacked = True
            self.invincibility_frames = 250
    def push(self, direction, strength=1, y=-1):
        self.velocity += pg.Vector2(direction * strength, y)
    def update(self, delta):
        if self.in_ground:
            self.timer -= delta
            if self.timer <= 0:
                return True
            return False

        for block in self.ground:
            if block.get_collision_rect().colliderect(pg.Rect(self.position, self.display.get_size())):
                self.in_ground = True

        self.invincibility_frames -= delta
        self.invincibility_frames = max(0, self.invincibility_frames)

        self.velocity.y += self.gravity

        self.position.x += self.velocity.x * delta / 5
        self.position.y += self.velocity.y * delta / 5

        self.time += delta

        self.display = pg.transform.rotate(pg.transform.flip(self.arrow,bool(math.copysign(1,self.velocity.x)-1),False), -math.copysign(1,self.velocity.x) * min(90, round(90/(500 ** 2) * self.time * self.time)))

    def get_collision_rect(self):
        return pg.Rect(self.position, self.display.get_size())

    def draw(self, surf):
        surf.blit(self.display, get_display_point(self.position))
