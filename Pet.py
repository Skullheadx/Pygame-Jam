from Actors import Actor

class Pet(Actor):
    width,height = 75,50

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)
    
    def update(self, delta, target):
        super().update(delta)

        self.follow_target(target)

        self.position, self.velocity = self.move_and_collide(self.position, self.velocity, delta)

