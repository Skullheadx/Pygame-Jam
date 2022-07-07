from Setup import *
from PhysicsBody import PhysicsBody
from Block import Block

class Actor:
    width, height = 50, 100
    colour = (76, 82, 92)
    speed = 0.2
    jump_strength = 1
    gravity = 0.098
    friction = 0.9
    

    def __init__(self, pos, collision_layer, collision_mask):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

        self.on_ground = False
        
        collision_layer.add(self)  # the layer the actor is on for collisions
        self.collision_layer = collision_layer
        self.collision_mask = collision_mask  # the layer the actor detects collisions against

        self.health = 100
        self.dead = False

        self.areas = dict()

        self.movable = False


    def update(self, delta):
        for area in self.areas.values():
            area.update(delta,self.position)

        if self.is_dead():
            return


        # Apply friction so the enemy isn't walking on ice
        if self.on_ground:
            self.velocity.x *= self.friction 

        # Apply gravity
        self.velocity.y += self.gravity

    def is_dead(self,reason=None):
        if self.health <= 0:
            self.dead = True


    def modify_health(self,amount, reason):
        self.health += amount
        self.is_dead(reason)

    def follow_target(self, node, follow_range=None, stop_dist=None):
        if stop_dist is None:
            stop_dist = max(self.height, self.width) * 1.5

        target = node.position

        # So that actor doesn't come up and hug u lol
        if (self.position - target).length_squared() < pow(stop_dist,2):
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

    def move_and_collide(self, pos, vel, delta):
        pos.x += vel.x * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:
            for thing in mask:
                if thing == self:
                    continue
                if collision_rect.colliderect(thing.get_collision_rect()):
                    print(self, vel, thing.velocity)
                    if thing.movable:
                        if vel.x > 0:
                            thing.position.x = pos.x + self.width
                        elif vel.x < 0:
                            thing.position.x = pos.x - thing.width
                    else:
                        if vel.x > 0:
                            pos.x = thing.position.x - self.width
                            vel.x = min(vel.x, 0)
                        elif vel.x < 0:
                            pos.x = thing.position.x + thing.width
                            vel.x = max(vel.x, 0)
                    collision_rect = self.get_collision_rect(pos)

        self.on_ground = False
        pos.y += vel.y * delta
        collision_rect = self.get_collision_rect(pos)
        for mask in self.collision_mask:        
            for thing in mask:
                if thing == self:
                    continue
                for area in self.areas.values():
                    if area.is_colliding(thing):
                        area.signal(thing)
                if collision_rect.colliderect(thing.get_collision_rect()):
                    if vel.y > 0:
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
        pg.draw.rect(surf, self.colour, get_display_rect(self.get_collision_rect()), border_radius=8)
        # pg.draw.rect(surf, (0,0,0), self.get_collision_rect(), border_radius=8, width=2)

        # Uncomment for debugging area hitboxes
        # for area in self.areas.values():
        #     area.draw(surf)
