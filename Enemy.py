from argparse import Action
from Setup import *
from Player import Player
from Actors import Actor
from Weapon import Melee


class Enemy(Actor):
    speed = Actor.speed * 0.5
    # jump_strength = Actor.jump_strength * 0.5
    colour = (235, 64, 52)
    friction = 0.9

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)

        self.areas = {
            "head": Area(self.position, pg.Vector2(self.width * 1 / 3 * 1 / 2, -2), self.width * 2 / 3, 25, Player,
                         self.knockout)}
        self.movable = False
        self.dizzy_time = 0

        self.direction = -1

        # self.health = 0 # for debugging without getting killed

        self.weapon = Melee(self.position, (-Melee.width / 2 + 7, Melee.height / 2 + self.height / 3 - 8),
                            (-5, Melee.height), self.width, -1, -10)

        self.buffer = []

    def update(self, delta, target=None):
        super().update(delta)
        if not self.attacked and target is not None and self.dizzy_time == 0:
            self.follow_target(target)
            if random.random() < 2/fps and not self.weapon.attacking and self.weapon.get_collision_rect().colliderect(target.get_collision_rect()):
                target.attack(self, self.weapon, self.direction)
                print('attack')
        self.dizzy_time -= delta
        self.dizzy_time = max(0, self.dizzy_time)

        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        if self.velocity.x == 0:
            self.direction = 0
        else:
            self.direction = math.copysign(1, self.velocity.x)
        self.weapon.update(delta, self.position, self.direction)

        # print(self.velocity)

    def knockout(self, node):
        self.dizzy_time = 100
        self.modify_health(-25, None)
        node.on_ground = False
        node.push(math.copysign(1, node.velocity.x), 0.25, -2.25)
        # self.crouch(1000)

    def draw(self, surf):
        self.weapon.draw(surf)
        super(Enemy, self).draw(surf)

        # for b in self.buffer:
        #     pg.draw.rect(surf,(0,0,255),b,3)
        # self.buffer.append(get_display_rect(self.get_collision_rect()))
        # pg.draw.rect(surf, (0, 255, 0), get_display_rect(self.get_collision_rect()), 2)
