import pygame.key

from Setup import *
from Actors import Actor

class Player(Actor):
    width, height = 25, 50
    colour = (52, 94, 235)
    speed = 0.2
    jump_strength = 0.9
    gravity = 0.098
    friction = 0.7
    

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)
        # self.areas = {"body":Area(self.position, pg.Vector2(0, self.height/2),self.width, self.height/2,Actor)}


    def update(self, delta):
        super().update(delta)

        # Get and handle input
        self.handle_input()

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

    def draw(self, surf):
        super().draw(surf)

    
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
