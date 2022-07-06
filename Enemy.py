from Setup import *
from Player import Player

class Enemy:
    width, height = 50, 100
    colour = (235, 64, 52)
    speed = 0.15
    jump_strength = 1
    gravity = 0.098
    friction = 0.9
    

    def __init__(self, pos, collision_layer, collision_mask):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

        self.on_ground = False
        
        collision_layer.add(self)  # the layer the enemy is on for collisions
        self.collision_mask = collision_mask  # the layer the enemy detects collisions against

        self.health = 100 # each instance of enemy has it's own unique health

        self.head_area = Area(self.position,pg.Vector2(0,-15), self.width, 25, Player)

        self.dizzy_time = 0

    def update(self, delta):

        # Apply friction so the enemy isn't walking on ice
        if self.on_ground:
            self.velocity.x *= self.friction 

        # Apply gravity
        self.velocity.y += self.gravity

        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position, self.velocity, delta)

        self.head_area.update(delta, self.position)

    def follow_player(self, player):
        target = player.position

        # So that enemy doesn't come up and hug u lol
        if (self.position - target).length_squared() < pow(self.width * 2,2):
            return


        if target.x < self.position.x:
            self.move_left()
        elif target.x > self.position.x:
            self.move_right()

        if target.y < self.position.y:
            self.jump()

    def jump(self):
        if self.on_ground:
            self.velocity.y = -self.jump_strength

    def move_left(self):
        self.velocity.x = -self.speed

    def move_right(self):
        self.velocity.x = self.speed

    def knockout(self):
        self.dizzy_time = 1000

    def move_and_collide(self, pos, vel, delta):
        pos.x += vel.x * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:
            for thing in mask:
                if thing == self:
                    continue
                if collision_rect.colliderect(thing.get_collision_rect()):
                    if vel.x > 0:
                        pos.x = thing.position.x - self.width
                        vel.x = min(vel.x + thing.velocity.x, 0)
                    elif vel.x < 0:
                        pos.x = thing.position.x + thing.width
                        vel.x = max(vel.x + thing.velocity.x, 0)
        self.on_ground = False
        pos.y += vel.y * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:        
            for thing in mask:
                if thing == self:
                    continue
                if collision_rect.colliderect(thing.get_collision_rect()):
                    if self.head_area.is_colliding(thing):
                        self.knockout()
                    if vel.y > 0:
                        pos.y = thing.position.y - self.height
                        vel.y = min(vel.y + thing.velocity.x, 0)
                        self.on_ground = True
                    elif vel.y < 0:
                        pos.y = thing.position.y + thing.height
                        vel.y = max(vel.y + thing.velocity.x, 0)
        return pos, vel

    def get_collision_rect(self, pos=None):
        if pos is None:
            pos = self.position
        return pg.Rect(pos, (self.width, self.height))

    def draw(self, surf):
        pg.draw.rect(surf, self.colour, self.get_collision_rect(), border_radius=15)
        self.head_area.draw(surf)
