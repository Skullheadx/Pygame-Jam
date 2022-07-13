import pygame.key

import Setup
from Setup import *
import time
from Actors import Actor
from datetime import datetime, timedelta
from Potion import Potion
from Item import PotionItem
from Spike import Spike
from Weapon import Sword
from Particle import Dust


class Player(Actor):
    friction = 0.2
    scale = 100
    factor = 640 / scale
    crop = pg.Rect(179, 169, 170, 401)
    idle_frames = [
        pg.transform.scale(pg.image.load(path.join("Assets/player/idle", file)).subsurface(pg.Rect(179, 169, 170, 401)),
                           (50, 100)) for file in listdir("Assets/player/idle")]

    attack_gif = Image.open("Assets/player/Sword_Slash.gif")
    attack_frames = []
    for i in range(attack_gif.n_frames):
        attack_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(attack_gif, i)), (200, 200)))
    run_gif = Image.open("Assets/player/Running_animation.gif")
    run_frames = []
    for i in range(run_gif.n_frames):
        run_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(run_gif, i)), (155, 155)))

    # Player SFX
    running_sound = pg.mixer.Sound("Assets/SFX/Running_Sound_Effect.wav")
    running_sound_channel = pg.mixer.Channel(1)
    sword_swing_sound = pg.mixer.Sound("Assets/SFX/Sword_Swing.wav")
    sword_swing_channel = pg.mixer.Channel(2)
    landing_sound = pg.mixer.Sound("Assets/SFX/Jump_Landing.wav")
    landing_sound_channel = pg.mixer.Channel(3)
    # Enemy SFX
    grunt_sound = pg.mixer.Sound("Assets/SFX/Grunt Sound.wav")
    skeleton_damaged_sound = pg.mixer.Sound("Assets/SFX/Skeleton_Damaged.wav")
    

    width, height = idle_frames[0].get_size()

    colour = (52, 94, 235)

    def __init__(self, pos, collision_layer, collision_mask, can_hurt, heals, spikes, arrows):
        super().__init__(pos, collision_layer, collision_mask)
        # self.initial_position = pg.Vector2(pos)
        # self.dashCooldown = timedelta(seconds=2, microseconds=500000)
        # self.timeBetweenDoublePress = timedelta(seconds=0, microseconds=500000)
        # self.dashSpeed = 5

        # self.dashPossible = False
        # self.lastDash = datetime.utcnow()
        # self.lastPressedLeft = datetime.utcnow()
        # self.lastValueL = False
        # self.lastPressedRight = datetime.utcnow()
        # self.lastValueR = False
        self.areas = {"head": Area(self.position, pg.Vector2(0, self.height / 2), self.width, self.height / 2, Actor),
                      "body": Area(self.position, (0, 0), self.width, self.height, PotionItem, self.add_potion),
                      "body2": Area(self.position, (0, 0), self.width, self.height, Spike, self.die)}

        self.spike_layer = spikes

        self.heal_layer = heals
        self.arrows = arrows

        self.potion_cooldown = 0
        self.starting_potions = 1
        self.potion_bag = [Potion(self)]
        for i in range(self.starting_potions - 1):
            self.potion_bag.append(Potion(self))  # use one liner

        self.weapon = Sword(self.position, (0, 0), self.width, -1)
        self.targets = can_hurt

        self.direction = -1

        self.state = "IDLE"
        self.previous_state = "IDLE"
        self.previous_ground_state = self.on_ground
        self.current_frame = 0
        self.display = self.idle_frames[0]
        self.display_offsets = {"weapon": pg.Vector2(0, 0), "player": pg.Vector2(0, 0)}

        self.buffer = []

    def die(self):
        self.dead = True

    def add_potion(self):
        if len(self.potion_bag) < 3:
            self.potion_bag.append(Potion(self))

    # def attack(self, enemy, weapon):
    #     super(Player, self).attack(enemy, weapon)
    #     self.current_frame = 0
    #     self.state = "ATTACK"
    #     print('a')

    def attack(self, enemy, weapon, direction):
        self.friction = 0.9

        super().attack(enemy, weapon, direction)

    def update(self, delta):

        if self.attacked:
            self.friction = 0.9
        else:
            self.friction = 0.2

        super().update(delta)

        # Get and handle input
        self.handle_input()

        for i, heal in enumerate(self.heal_layer):
            if len(self.potion_bag) < 3 and self.areas["body"].is_colliding(heal):
                self.add_potion()
                self.heal_layer.remove(heal)
                break

        for i in self.spike_layer:
            if self.areas["body2"].is_colliding(i):
                self.die()

        if len(self.potion_bag) > 0:
            self.potion_bag[0].get_input(self)

        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        prev_direction = self.direction
        # if self.velocity.x == 0:
        #     self.direction = 0
        # else:
        #     self.direction = math.copysign(1, self.velocity.x)
        self.direction = math.copysign(1, pg.mouse.get_pos()[0] - get_display_point(self.position).x)
        self.weapon.update(delta, self.position, self.direction)
        for arrow in self.arrows:
            if (not arrow.used) and (not arrow.in_ground) and (not self.attacked) and (self.invincibility_frames == 0) and self.get_collision_rect().colliderect(self.get_collision_rect()):
                self.modify_health(-1, "arrow")
                arrow.used = True
                self.attacked = True
                self.invincibility_frames = self.invincibility_time
        if self.velocity.x == 0 and self.state == "RUN":
            self.state = "IDLE"

        if self.on_ground == True and self.previous_ground_state == False:
            self.landing_sound_channel.play(self.landing_sound)

        if self.state == "IDLE":
            self.display_offsets["player"] = pg.Vector2(0, 0)

            frame = math.floor(self.current_frame)
            if self.direction == 1:
                self.display = self.idle_frames[math.floor(frame)]
            elif self.direction == -1:
                self.display = pg.transform.flip(self.idle_frames[math.floor(frame)], True, False)
            else:
                self.direction = prev_direction
                if prev_direction == 1:
                    self.display = self.idle_frames[math.floor(frame)]
                elif prev_direction == -1:
                    self.display = pg.transform.flip(self.idle_frames[math.floor(frame)], True, False)
            # 1 - 10 up, 11 down by 1, 12 - 18 down by 2, 19-20 down 1 FIX THIS
            frame += 1
            if 3 < frame < 12:
                self.display_offsets["weapon"] = pg.Vector2(3, -2)
            else:
                self.display_offsets["weapon"] = pg.Vector2(3, -5)
            self.current_frame = (self.current_frame + 0.1) % len(self.idle_frames)
        elif self.state == "ATTACK":
            frame = math.floor(self.current_frame)
            if self.direction == 1:
                self.display = self.attack_frames[math.floor(frame)]
                self.display_offsets["player"] = pg.Vector2(-50, -50)

            elif self.direction == -1:
                self.display = pg.transform.flip(self.attack_frames[math.floor(frame)], True, False)
                self.display_offsets["player"] = pg.Vector2(-100, -50)

            else:
                self.direction = prev_direction
                if prev_direction == 1:
                    self.display_offsets["player"] = pg.Vector2(-50, -50)

                    self.display = self.attack_frames[math.floor(frame)]
                elif prev_direction == -1:
                    self.display = pg.transform.flip(self.attack_frames[math.floor(frame)], True, False)
                    self.display_offsets["player"] = pg.Vector2(-100, -50)

            self.current_frame += 0.4
            if math.floor(self.current_frame) == self.attack_gif.n_frames:
                self.state = "IDLE"
        elif self.state == "RUN":
            frame = math.floor(self.current_frame)
            if self.velocity.x > 0:
                self.display = self.run_frames[math.floor(frame)]
                self.display_offsets["player"] = pg.Vector2(-40, -35)
            elif self.velocity.x < 0:
                self.display = pg.transform.flip(self.run_frames[math.floor(frame)], True, False)
                self.display_offsets["player"] = pg.Vector2(-65, -35)

            if frame % 2 == 0 and self.on_ground:
                Dust(pg.Vector2(self.get_collision_rect().midbottom) + pg.Vector2(
                    math.copysign(1, self.velocity.x) * -self.width / 2, -15), 16, self.direction)

            self.current_frame = (self.current_frame + 0.3) % self.run_gif.n_frames

        if self.state == "RUN":
            if self.previous_state != "RUN":
                self.running_sound_channel.play(self.running_sound, -1)

            if self.on_ground == True and self.previous_ground_state == False:
                self.running_sound_channel.play(self.running_sound, -1)

        self.previous_state = self.state
        self.previous_ground_state = self.on_ground
        return self.position - center

    def handle_input(self):
        if self.stun_time > 0:
            return

        pressed = pygame.key.get_pressed()
        if pressed[pg.K_w] or pressed[pg.K_UP] or pressed[pg.K_SPACE]:
            self.jump()
            self.running_sound_channel.stop()
        if pressed[pg.K_a] or pressed[pg.K_LEFT]:
            if self.state != "ATTACK":
                if self.state != "RUN":
                    self.current_frame = 0

                self.state = "RUN"
            self.move_left()
            # if (self.lastValueL == False):
            #     timeSincePressed = datetime.utcnow() - self.lastPressedLeft
            #     timeSinceLastDash = datetime.utcnow() - self.lastDash
            #     if (timeSinceLastDash >= self.dashCooldown):
            #         self.dashPossible = False # True to enable dash
            #     else:
            #         self.dashPossible = False
            #     if (timeSincePressed < self.timeBetweenDoublePress and self.dashPossible == True):
            #         self.move_left(
            #             self.dashSpeed)  # change this to change how the player dashes (maybe replace with a custom dash function)
            #         self.dashPossible = False
            #         self.lastDash = datetime.utcnow()
            #     self.lastPressedLeft = datetime.utcnow()

        elif pressed[pg.K_d] or pressed[pg.K_RIGHT]:
            if self.state != "ATTACK":
                if self.state != "RUN":
                    self.current_frame = 0

                self.state = "RUN"

            self.move_right()
            # if (self.lastValueR == False):
            #     timeSincePressed = datetime.utcnow() - self.lastPressedRight
            #     timeSinceLastDash = datetime.utcnow() - self.lastDash
            #     if (timeSinceLastDash >= self.dashCooldown):
            #         self.dashPossible = False # True to enable dash
            #     else:
            #         self.dashPossible = False
            #     if (timeSincePressed < self.timeBetweenDoublePress and self.dashPossible == True):
            #         self.lastDash = datetime.utcnow()
            #         self.dashPossible = False
            #         self.move_right(
            #             self.dashSpeed)  # change this to change how the player dashes (maybe replace with a custom dash function)
            #     self.lastPressedRight = datetime.utcnow()
        else:
            if self.state == "RUN":
                self.state = "IDLE"
            self.running_sound_channel.stop()

        # self.lastValueL = pressed[pg.K_a] or pressed[pg.K_LEFT]
        # self.lastValueR = pressed[pg.K_d] or pressed[pg.K_RIGHT]

        mouse_pressed = pg.mouse.get_pressed(3)
        if mouse_pressed[0]:  # LMB
            if self.state != "ATTACK":
                self.state = "ATTACK"
                self.current_frame = 0
                # self.sword_swing_channel.stop()
                self.sword_swing_channel.play(self.sword_swing_sound)
        if self.state == "ATTACK":
            if 12 > math.floor(self.current_frame) > 6:
                for mask in self.targets:
                    for enemy in mask:
                        # if not enemy.attacked and self.weapon.get_collision_rect().colliderect(
                        #         enemy.get_collision_rect()):

                        if not enemy.attacked and get_display_rect(self.weapon.get_collision_rect()).colliderect(
                                get_display_rect(enemy.get_collision_rect())):
                            enemy_type = str(type(enemy))
                            if enemy.health > 0:
                                if enemy_type == "<class 'Enemy.Enemy'>":
                                    pg.mixer.Sound.play(self.grunt_sound)
                                if enemy_type == "<class 'Enemy.Skeleton'>":
                                    pg.mixer.Sound.play(self.skeleton_damaged_sound)
                            enemy.attack(self, self.weapon, self.direction)
                for arrow in self.arrows:
                    if not arrow.attacked and get_display_rect(self.weapon.get_collision_rect()).colliderect(
                            get_display_rect(arrow.get_collision_rect())):
                        arrow.attack(self, self.weapon, self.direction)

    def draw(self, surf):
        # super().draw(surf)
        if self.state == "IDLE":
            # self.weapon.draw(surf, self.display_offsets["weapon"])
            if self.direction == 1:
                surf.blit(pg.transform.flip(self.weapon.img, True, True),
                          get_display_rect(self.get_collision_rect()).topleft + pg.Vector2(-25, 55) +
                          self.display_offsets["weapon"])
            elif self.direction == -1:
                surf.blit(pg.transform.flip(self.weapon.img, False, True),
                          get_display_rect(self.get_collision_rect()).topleft + pg.Vector2(0, 55) +
                          self.display_offsets["weapon"])
        elif self.state == "RUN":
            # self.weapon.draw(surf, self.display_offsets["weapon"])
            if self.velocity.x > 0:
                surf.blit(pg.transform.flip(self.weapon.img2, True, True),
                          get_display_rect(self.get_collision_rect()).topleft + pg.Vector2(-25, 25) +
                          self.display_offsets["weapon"])
            else:
                surf.blit(pg.transform.flip(self.weapon.img2, False, True),
                          get_display_rect(self.get_collision_rect()).topleft + pg.Vector2(0, 25) +
                          self.display_offsets["weapon"])

        a = get_display_rect(self.get_collision_rect())
        b = a.topleft + self.display_offsets["player"]
        if pg.Rect(b, a.size).colliderect(screen_rect):
            surf.blit(self.display, b)
        #
        # for b in self.buffer:
        #     pg.draw.rect(surf,(0,0,255),get_display_rect(b),3)
        # self.buffer.append(self.get_collision_rect())

        # print(self, self.position)
        # super().draw(surf)
        # print(self.position, self.velocity, get_display_rect(self.get_collision_rect()).topleft, Setup.camera_offset)
        # pg.draw.rect(surf, self.colour, get_display_rect(self.get_collision_rect()), border_radius=8)
        # pg.draw.rect(surf, (255, 0, 0), get_display_rect(self.weapon.get_collision_rect()), width=3)

        # pg.draw.rect(surf, (0, 255, 0), get_display_rect(self.get_collision_rect()), 2)

        # pg.draw.rect(surf,self.colour,pg.Rect(center, (self.width, self.height)),border_radius=8)

        # # Healthbar Stuff
        # # bar is made of 2 rectanges, background which is just a simple rectange and foreground which goes on top and has a bit of math involved
        # background_rect = pg.Rect(20, 20, 1080 * 0.2, 640 * 0.08)

        # # idea is that 1080*0.185 = size of bar at 100% hp, at lower hp you want to get a fraction of that which is why we multiply by (health*0.01) example: 70 hp * 0.01 = 0.7
        # foreground_rect = pg.Rect(0, 0, 1080 * 0.185 * (self.health * 0.01), 640 * 0.06)
        # # make sure the red part health bar always sits on the left
        # # sets bar to center of background bar, then subtracts 1/2 of blank space to put it on the left
        # foreground_rect.center = (
        #     background_rect.centerx - 1080 * 0.185 * ((1 - self.health * 0.01) / 2), background_rect.centery)
        # pg.draw.rect(surf, (54, 54, 54), background_rect)
        # pg.draw.rect(surf, red, foreground_rect)

        # # text
        # current_health_display = createText(0, 0, 30, white, "Regular", str(self.health) + "/100")[0]
        # text_rect = current_health_display.get_rect(center=background_rect.center)
        # surf.blit(current_health_display, text_rect)

    def potion_cooldown_timer(self):
        while self.potion_cooldown > 0:
            self.potion_cooldown -= 1
            # print(self.potion_cooldown)
            time.sleep(1)
