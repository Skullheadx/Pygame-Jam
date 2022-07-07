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
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity, delta)
        return self.velocity * delta

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pg.K_w] or pressed[pg.K_UP] or pressed[pg.K_SPACE]:
            self.jump()
        if pressed[pg.K_a] or pressed[pg.K_LEFT]:
            self.move_left()
        if pressed[pg.K_d] or pressed[pg.K_RIGHT]:
            self.move_right()
<<<<<<< Updated upstream
=======
            if(self.lastValueR == False):
                timeSincePressed = datetime.utcnow() - self.lastPressedRight
                timeSinceLastDash = datetime.utcnow() - self.lastDash
                if(timeSinceLastDash >= self.dashCooldown):     self.dashPossible = True
                else:   self.dashPossible = False
                if(timeSincePressed < self.timeBetweenDoublePress and self.dashPossible == True):
                    self.lastDash = datetime.utcnow()
                    self.dashPossible = False
                    self.move_right(self.dashSpeed) # change this to change how the player dashes (maybe replace with a custom dash function)
                self.lastPressedRight = datetime.utcnow()        
        
        self.lastValueL = pressed[pg.K_a] or pressed[pg.K_LEFT]
        self.lastValueR = pressed[pg.K_d] or pressed[pg.K_RIGHT]

    def attack(self, enemy, weapon):
        self.modify_health(-10,"enemy")
        self.push(enemy.velocity)
>>>>>>> Stashed changes

    def draw(self, surf):
        super().draw(surf)
        # pg.draw.rect(surf,self.colour,pg.Rect(center, (self.width, self.height)),border_radius=8)

        # Healthbar Stuff
        # bar is made of 2 rectanges, background which is just a simple rectange and foreground which goes on top and has a bit of math involved
        background_rect = pg.Rect(20, 20, 1080 * 0.2, 640 * 0.08)

        # idea is that 1080*0.185 = size of bar at 100% hp, at lower hp you want to get a fraction of that which is why we multiply by (health*0.01) example: 70 hp * 0.01 = 0.7
        foreground_rect = pg.Rect(0, 0, 1080 * 0.185 * (self.health * 0.01), 640 * 0.06)
        # make sure the red part health bar always sits on the left
        # sets bar to center of background bar, then subtracts 1/2 of blank space to put it on the left
        foreground_rect.center = (
        background_rect.centerx - 1080 * 0.185 * ((1 - self.health * 0.01) / 2), background_rect.centery)
        pg.draw.rect(surf, (54, 54, 54), background_rect)
        pg.draw.rect(surf, (255, 0, 0), foreground_rect)

        # text
        font = pg.font.Font("Font/Exo2-Regular.ttf", 30)
        current_health = str(self.health) + "/100"
        current_health_display = font.render(current_health, True, (255, 255, 255))
        text_rect = current_health_display.get_rect(center=background_rect.center)
        surf.blit(current_health_display, text_rect)
