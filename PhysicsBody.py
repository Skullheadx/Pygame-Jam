from Setup import *
from Block import Block
from Function.createText import createText
from Actors import Actor


class PhysicsBody:
    gravity = Actor.gravity
    friction = Actor.friction
    invincibility_time = 150

    def __init__(self, pos, vel, width, height, colour, collision_layer, collision_mask):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(vel)
        self.width, self.height = height, width
        self.colour = colour

        self.on_ground = False

        self.dead = False

        self.movable = True
        self.attacked = False
        self.invincibility_frames = 0

        collision_layer.add(self)  # the layer the actor is on for collisions
        self.collision_layer = collision_layer
        self.collision_mask = collision_mask  # the layer the actor detects collisions against

    def update(self, delta, test=None, test2=None):
        if self.on_ground:
            self.velocity.x *= self.friction

        self.velocity.y += self.gravity


        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        if self.on_ground:
            self.attacked = False

    def attack(self, enemy, weapon, direction):
        self.push(direction, 2, -1)
        self.attacked = True
        self.invincibility_frames = self.invincibility_time

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
                    # if thing.movable:
                    #     if vel.x > 0:
                    #         thing.position.x = pos.x + self.width
                    #     elif vel.x < 0:
                    #         thing.position.x = pos.x - thing.width
                    if vel.x > 0:
                        pos.x = thing.position.x - self.width
                        # vel.x = min(vel.x, 0)
                    elif vel.x < 0:
                        pos.x = thing.position.x + thing.width
                        # vel.x = max(vel.x, 0)
                    collision_rect = self.get_collision_rect(pos)

        self.on_ground = False
        pos.y += vel.y * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:
            for thing in mask:
                if thing == self:
                    continue
                if collision_rect.colliderect(thing.get_collision_rect()):
                    if vel.y > 0:
                        pos.y = thing.position.y - self.height
                        vel.y = min(vel.y, 0)
                        self.on_ground = True
                    elif vel.y < 0:
                        pos.y = thing.position.y + thing.height
                        # vel.y = max(vel.y, 0)
                    # collision_rect = self.get_collision_rect(pos)
        return pos, vel

    def get_collision_rect(self, pos=None):
        if pos is None:
            pos = self.position
        return pg.Rect(pos, (self.width, self.height))

    def draw(self, surf):
        # print(self.position, self.velocity)
        pg.draw.rect(surf, self.colour, get_display_rect(self.get_collision_rect()), border_radius=8)
