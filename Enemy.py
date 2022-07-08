from argparse import Action
from Setup import *
from Player import Player
from Actors import Actor
from Weapon import Melee

class Enemy(Actor):
    width, height = 50, 100
    colour = (235, 64, 52)
    speed = 0.2
    jump_strength = 0.75
    gravity = 0.098
    friction = 0.9
    

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)

        self.areas = {"head":Area(self.position,pg.Vector2(self.width * 1/3 * 1/2,-2), self.width * 2/3, 25, Player, self.knockout)}
        self.movable = True
        self.dizzy_time = 0

        # self.health = 0

        self.weapon = Melee(self.position, (-Melee.width/2 + 7, Melee.height/2 + self.height/3 - 8), (-5,Melee.height), self.width,-1)

    def update(self, delta, target=None):
        super().update(delta)
        if target is not None and self.dizzy_time == 0:
            self.follow_target(target,stop_dist=self.weapon.width * 0.8 + self.width + target.width)
            if random.random() < 3/fps and not self.weapon.attacking and self.weapon.get_collision_rect().colliderect(target.get_collision_rect()):
                self.weapon.swing()
                target.attack(self, self.weapon)
        self.dizzy_time -= delta
        self.dizzy_time = max(0,self.dizzy_time)


        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        if self.velocity.x == 0:
            direction = 0
        else:
            direction = math.copysign(1,self.velocity.x)
        self.weapon.update(delta,self.position, direction)

    def knockout(self, node):
        self.dizzy_time = 100
        self.modify_health(-25, None)
        node.push2(math.copysign(1,self.velocity.x))
        # self.crouch(1000)

    def draw(self, surf):
        self.weapon.draw(surf)
        super(Enemy, self).draw(surf)
