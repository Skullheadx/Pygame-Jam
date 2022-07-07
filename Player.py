import pygame.key

import Setup
import time
import threading
from Setup import *
from Actors import Actor
from datetime import datetime, timedelta
from Potion import Potion

class Player(Actor):
    width, height = 25, 50
    colour = (52, 94, 235)
    speed = 0.2
    jump_strength = 0.9
    gravity = 0.098
    friction = 0.7

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)
        self.initial_position = pg.Vector2(pos)
        self.dashCooldown = timedelta(seconds=2, microseconds=500000)
        self.timeBetweenDoublePress = timedelta(seconds=0, microseconds=500000)
        self.dashSpeed = 5

        self.dashPossible = True
        self.lastDash = datetime.utcnow()
        self.lastPressedLeft = datetime.utcnow()
        self.lastValueL = False
        self.lastPressedRight = datetime.utcnow()
        self.lastValueR = False
        # self.areas = {"body":Area(self.position, pg.Vector2(0, self.height/2),self.width, self.height/2,Actor)}

        self.potion_cooldown = 0
        self.starting_potions = 999
        self.potion_bag = [Potion(self)]
        for i in range(self.starting_potions):
            self.potion_bag.append(Potion(self))

    def update(self, delta):
        super().update(delta)

        # Get and handle input
        self.handle_input()

        #if self.potion_cooldown > 0:
            #threading.Thread(Potion.cooldown)

        if len(self.potion_bag) > 0:
            self.potion_bag[0].get_input(self)

        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)
        return self.position - self.initial_position

        

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pg.K_w] or pressed[pg.K_UP] or pressed[pg.K_SPACE]:
            self.jump()
        if pressed[pg.K_a] or pressed[pg.K_LEFT]:
            self.move_left()
            if(self.lastValueL == False):
                timeSincePressed = datetime.utcnow() - self.lastPressedLeft
                timeSinceLastDash = datetime.utcnow() - self.lastDash
                if(timeSinceLastDash >= self.dashCooldown): self.dashPossible = True
                else: self.dashPossible = False
                if(timeSincePressed < self.timeBetweenDoublePress and self.dashPossible == True):
                    self.move_left(self.dashSpeed) # change this to change how the player dashes (maybe replace with a custom dash function)
                    self.dashPossible = False
                    self.lastDash = datetime.utcnow()
                self.lastPressedLeft = datetime.utcnow()            
            
        if pressed[pg.K_d] or pressed[pg.K_RIGHT]:
            self.move_right()
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

    def draw(self, surf):
        super().draw(surf)
        # print(self.position, self.velocity, get_display_rect(self.get_collision_rect()).topleft, Setup.camera_offset)
        # pg.draw.rect(surf, self.colour, get_display_rect(self.get_collision_rect()), border_radius=8)

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
