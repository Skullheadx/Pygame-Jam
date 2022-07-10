import pygame.key

from Setup import *
from Actors import Actor


class Player(Actor):
    width, height = 25, 50
    colour = (52, 94, 235)
<<<<<<< Updated upstream
    speed = 0.2
    jump_strength = 0.9
    gravity = 0.098
    friction = 0.7
=======
>>>>>>> Stashed changes

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)
<<<<<<< Updated upstream
        # self.areas = {"body":Area(self.position, pg.Vector2(0, self.height/2),self.width, self.height/2,Actor)}
=======
        # self.initial_position = pg.Vector2(pos)
        self.dashCooldown = timedelta(seconds=2, microseconds=500000)
        self.timeBetweenDoublePress = timedelta(seconds=0, microseconds=500000)
        self.dashSpeed = 10

        self.dashPossible = True
        self.lastDash = datetime.utcnow()
        self.lastPressedLeft = datetime.utcnow()
        self.lastValueL = False
        self.lastPressedRight = datetime.utcnow()
        self.lastValueR = False
        self.areas = {"body": Area(self.position, pg.Vector2(0, self.height / 2), self.width, self.height / 2, Actor),
                      "head": Area(self.position, pg.Vector2(self.width * 1 / 3 * 1 / 2, -2), self.width * 2 / 3, 25,
                                   Actor)}

        self.potion_cooldown = 0
        self.starting_potions = 999
        self.potion_bag = [Potion(self)]
        for i in range(self.starting_potions):
            self.potion_bag.append(Potion(self)) # use one liner

        self.weapon = Melee(self.position, (-Melee.width / 2 + 7, Melee.height / 2 + self.height / 3 - 8),
                            (-5, Melee.height), self.width, -1, -25)
        self.targets = can_hurt

        self.direction = -1

        self.state = "IDLE"
        self.current_frame = 0
        self.display = self.idle_frames[0]
        self.display_offsets = {"weapon": pg.Vector2(0, 0)}
>>>>>>> Stashed changes

    def update(self, delta):
        super().update(delta)

        # Get and handle input
        self.handle_input()

        # Deals with collision and applying velocity
<<<<<<< Updated upstream
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity, delta)
        return self.velocity * delta
=======
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        prev_direction = self.direction
        if self.velocity.x == 0:
            self.direction = 0
        else:
            self.direction = math.copysign(1, self.velocity.x)
        self.weapon.update(delta, self.position, self.direction)

        if self.state == "IDLE":
            frame = math.floor(self.current_frame)
            if self.direction == 1:
                self.display = self.idle_frames[math.floor(frame)]
            elif self.direction == -1:
                self.display = pg.transform.flip(self.idle_frames[math.floor(frame)], True, False)
            else:
                if prev_direction == 1:
                    self.display = self.idle_frames[math.floor(frame)]
                elif prev_direction == -1:
                    self.display = pg.transform.flip(self.idle_frames[math.floor(frame)], True, False)
                self.direction = prev_direction
            # 1 - 10 up, 11 down by 1, 12 - 18 down by 2, 19-20 down 1 FIX THIS
            frame += 1
            if 1 < frame < 10:
                self.display_offsets["weapon"] = pg.Vector2(0, 2)
            elif frame == 11 or frame == 19 or frame == 20:
                self.display_offsets["weapon"] = pg.Vector2(0, 1)
            else:
                self.display_offsets["weapon"] = pg.Vector2(0, 0)
            self.current_frame = (self.current_frame + 0.1) % len(self.idle_frames)

        print()
        return self.position - pg.Vector2(SCREEN_WIDTH/3, SCREEN_HEIGHT / 2)

>>>>>>> Stashed changes

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
