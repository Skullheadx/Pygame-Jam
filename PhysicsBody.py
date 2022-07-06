from Setup import *
from Block import Block

class PhysicsBody:
    speed = 0.2
    jump_strength = 1
    gravity = 0.098
    friction = 0.9

    def __init__(self, pos, vel, width, height, colour, collision_layer, collision_mask):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(vel)
        self.width, self.height = width, height
        self.colour = colour

        self.on_ground = False

        self.dead = False

        self.movable =True

        collision_layer.add(self)  # the layer the actor is on for collisions
        self.collision_layer = collision_layer
        self.collision_mask = collision_mask  # the layer the actor detects collisions against

    def update(self, delta, test=None):
        # Apply friction so the enemy isn't walking on ice
        if self.on_ground:
            self.velocity.x *= self.friction

        # Apply gravity
        self.velocity.y += self.gravity

        self.position, self.velocity = self.move_and_collide(self.position, self.velocity, delta)

    def move_and_collide(self, pos, vel, delta):
        pos.x += vel.x * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:
            for thing in mask:
                if thing == self:
                    continue
                if collision_rect.colliderect(thing.get_collision_rect()):
                    if thing.movable:
                        thing.velocity.x = vel.x
                    if vel.x > 0:
                        pos.x = thing.position.x - self.width
                        vel.x = min(vel.x + thing.velocity.x, 0)
                    elif vel.x < 0:
                        pos.x = thing.position.x + thing.width
                        vel.x = max(vel.x + thing.velocity.x, 0)
                    collision_rect = self.get_collision_rect(pos)
        self.on_ground = False
        pos.y += vel.y * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:
            for thing in mask:
                if thing == self:
                    continue
                if collision_rect.colliderect(thing.get_collision_rect()):
                    if thing.movable:
                        thing.velocity.y += vel.y

                    if vel.y > 0:
                        pos.y = thing.position.y - self.height
                        vel.y = min(vel.y + thing.velocity.y, 0)
                        self.on_ground = True
                    elif vel.y < 0:
                        pos.y = thing.position.y + thing.height
                        vel.y = max(vel.y + thing.velocity.y, 0)
                    collision_rect = self.get_collision_rect(pos)
        return pos, vel

    def get_collision_rect(self, pos=None):
        if pos is None:
            pos = self.position
        return pg.Rect(pos, (self.width, self.height))

    def draw(self, surf):
        # print(self.position, self.velocity)
        pg.draw.rect(surf, self.colour, self.get_collision_rect(), border_radius=8)