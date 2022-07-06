import pygame.key

from Setup import *


class Player:
    width, height = 50, 100
    colour = (52, 94, 235)
    speed = 0.3
    jump_strength = 1.5
    gravity = 0.098
    friction = 0.9
    

    def __init__(self, pos, collision_layer, collision_mask):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

        self.on_ground = False

        collision_layer.add(self)  # the layer the player is on for collisions
        self.collision_mask = collision_mask  # the layer the player detects collisions against

        self.health = 100 # each instance of player has it's own unique health

    def update(self, delta):
        # Get and handle input
        self.handle_input()

        # Apply friction so the player isn't walking on ice
        if self.on_ground:
            self.velocity.x *= self.friction 

        # Apply gravity
        self.velocity.y += self.gravity

        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position, self.velocity, delta)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pg.K_w] or pressed[pg.K_UP] or pressed[pg.K_SPACE]:
            self.jump()
        if pressed[pg.K_a] or pressed[pg.K_LEFT]:
            self.move_left()
        if pressed[pg.K_d] or pressed[pg.K_RIGHT]:
            self.move_right()

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

    
        #Healthbar Stuff
        # self.position is the top left   

        background_rect = pg.Rect(0, 0, 1080*0.2, 640*0.08)
        background_rect.center = (1080*0.5, 50)
        foreground_rect = pg.Rect(0, 0, 1080*0.19, 640*0.07)
        foreground_rect.center = background_rect.center
        pg.draw.rect(surf, (54, 54, 54), background_rect)
        pg.draw.rect(surf, (255, 0, 0), foreground_rect)
        
        font = pg.font.Font(None , 20)
        current_health = str(self.health) + "/100"
        current_health_display = font.render(current_health, True, (255, 255, 255))
        surf.blit(current_health_display, foreground_rect)
    
