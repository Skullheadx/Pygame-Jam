from argparse import Action
from Setup import *
from Player import Player
from Actors import Actor

class Enemy(Actor):
    width, height = 50, 100
    colour = (235, 64, 52)
    speed = 0.2
    jump_strength = 1.1
    gravity = 0.098
    friction = 0.9
    

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)

        self.areas = {"head":Area(self.position,pg.Vector2(0,-15), self.width, 25, Player, self.knockout)}

        self.dizzy_time = 0

    def update(self, delta, target=None):
        super().update(delta)
        if target is not None and self.dizzy_time == 0:
            self.follow_target(target)
        self.dizzy_time -= delta
        self.dizzy_time = max(0,self.dizzy_time)

        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position, self.velocity, delta)

    def knockout(self, node):
        self.dizzy_time = 10000

