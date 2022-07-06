from Actors import Actor
from Player import Player

class Pet(Actor):
    width,height = 35,25
    speed = Player.speed * 0.75
    jump_strength = Player.jump_strength / 2

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)
    
    def update(self, delta, target):
        super().update(delta)

        self.follow_target(target, stop_dist=70)

        self.position, self.velocity = self.move_and_collide(self.position, self.velocity, delta)
