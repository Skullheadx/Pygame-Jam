import math
from argparse import Action
from Setup import *
from Player import Player
from Actors import Actor
from Weapon import Sword, Lightning
from RangedAttack import RangedAttack
from Particle import Dust

class Enemy(Actor):
    speed = Actor.speed * 0.4
    jump_strength = Actor.jump_strength * 1.1
    colour = (235, 64, 52)
    friction = 0.9
    run_gif = Image.open("Assets/enemy/Goon_Run.gif")
    run_frames = []
    for i in range(run_gif.n_frames):
        run_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(run_gif, i)), (180, 180)))

    attack_gif = Image.open("Assets/enemy/Goon_attack.gif")
    attack_frames = []
    for i in range(attack_gif.n_frames):
        attack_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(attack_gif, i)), (180, 180)))

    #SFX
    # player_grunt = pg.mixer.Sound("Assets/SFX/Player Grunt.wav")
    # player_grunt_channel = pg.mixer.Channel(4)

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)

        self.areas = {
            "head": Area(self.position, pg.Vector2(self.width * 1 / 3 * 1 / 2, -2), self.width * 2 / 3, 25, Player,
                         self.knockout)}
        self.movable = False

        self.direction = -1
        self.prev_direction = self.direction

        # self.health = 0 # for debugging without getting killed

        self.weapon = Sword(self.position, (0, 0), self.width, -1)


        self.buffer = []

        self.display_offsets = {"enemy":pg.Vector2(0,0)}

        self.current_frame = 0
        self.display = self.run_frames[math.floor(self.current_frame)]
        self.state = "RUN"
        
    def update(self, delta, target=None):
        super().update(delta)
        if not self.attacked and target is not None and self.stun_time == 0:
            self.follow_target(target, follow_range=750,stop_dist=target.width/2+self.weapon.width)
            if not target.attacked and get_display_rect(self.weapon.get_collision_rect()).colliderect(
                    get_display_rect(target.get_collision_rect())):
                if self.state != "ATTACK":
                    self.state = "ATTACK"
                    self.current_frame = 0
                elif 4 < self.current_frame:
                    target.attack(self, self.weapon, self.direction)
                    # self.player_grunt_channel.play(self.player_grunt)
        #
        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        self.prev_direction = self.direction
        if self.velocity.x == 0:
            self.direction = self.prev_direction
        else:
            self.direction = math.copysign(1, self.velocity.x)
        self.weapon.update(delta, self.position, self.direction)
        
        if self.state == "RUN":
            frame = math.floor(self.current_frame)
            if self.velocity.x > 0:
                self.display = self.run_frames[math.floor(frame)]
                self.display_offsets["enemy"] = pg.Vector2(-30, -35)
            elif self.velocity.x <= 0:
                self.display = pg.transform.flip(self.run_frames[math.floor(frame)], True, False)
                self.display_offsets["enemy"] = pg.Vector2(-90, -35)
            if frame % 4 == 0 and self.on_ground:
                Dust(pg.Vector2(self.get_collision_rect().midbottom) + pg.Vector2(math.copysign(1, self.velocity.x) * -self.width/2,-15), 16, self.direction)
            self.current_frame = (self.current_frame + 0.25) % self.run_gif.n_frames
        elif self.state == "ATTACK":
            frame = math.floor(self.current_frame)
            if self.direction == 1:
                self.display = pg.transform.flip(self.attack_frames[math.floor(frame)], False, False)
                self.display_offsets["enemy"] = pg.Vector2(-50, -50)
            else:
                self.display = pg.transform.flip(self.attack_frames[math.floor(frame)], True, False)
                self.display_offsets["enemy"] = pg.Vector2(-80, -50)
            self.current_frame += 0.4
            if math.floor(self.current_frame) >= self.attack_gif.n_frames-1:
                self.state = "RUN"
                self.current_frame = 0

        # print(self.velocity)

    def knockout(self, node):
        self.stun_time = 100
        self.modify_health(-25, None)
        node.on_ground = False
        node.push(math.copysign(1, node.velocity.x), 0.25, -2.25)
        # self.crouch(1000)

    def draw(self, surf):
        # self.weapon.draw(surf)
        # super(Enemy, self).draw(surf)
        surf.blit(self.display, get_display_rect(self.get_collision_rect()).topleft + self.display_offsets["enemy"])

        # for b in self.buffer:
        #     pg.draw.rect(surf,(0,0,255),get_display_rect(b),3)
        # self.buffer.append(self.get_collision_rect())
        # pg.draw.rect(surf, (0, 255, 0), get_display_rect(self.get_collision_rect()), 2)


class Skeleton(Actor):
    speed = Actor.speed * 0.4
    jump_strength = Actor.jump_strength * 1.1
    colour = (235, 64, 52)
    friction = 0.9
    run_gif = Image.open("Assets/skeleton/skeleton_run.gif")
    run_frames = []
    for i in range(run_gif.n_frames):
        run_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(run_gif, i)), (170, 138)))

    attack_gif = Image.open("Assets/skeleton/skeleton_attack.gif")
    attack_frames = []
    for i in range(attack_gif.n_frames):
        attack_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(attack_gif, i)), (170, 138)))
    # player_grunt = pg.mixer.Sound("Assets/SFX/Player Grunt.wav")
    # player_grunt_channel = pg.mixer.Channel(4)

    player_grunt = pg.mixer.Sound("Assets/SFX/Player Grunt.wav")
    player_grunt_channel = pg.mixer.Channel(4)

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)

        self.areas = {
            "head": Area(self.position, pg.Vector2(self.width * 1 / 3 * 1 / 2, -2), self.width * 2 / 3, 25, Player,
                         self.knockout)}
        self.movable = False

        self.direction = -1
        self.prev_direction = self.direction

        # self.health = 75
        self.health = 0 # for debugging without getting killed

        self.weapon = Sword(self.position, (0, 0), self.width, -1)


        self.buffer = []

        self.display_offsets = {"enemy":pg.Vector2(0,0)}

        self.current_frame = 0
        self.display = self.run_frames[math.floor(self.current_frame)]
        self.state = "RUN"

    def update(self, delta, target=None):
        super().update(delta)
        if not self.attacked and target is not None and self.stun_time == 0:
            self.follow_target(target, follow_range=750,stop_dist=target.width/2+self.weapon.width)
            if not target.attacked and get_display_rect(self.weapon.get_collision_rect()).colliderect(
                    get_display_rect(target.get_collision_rect())):
                if self.state != "ATTACK":
                    self.state = "ATTACK"
                    self.current_frame = 0
                elif 4 < self.current_frame:
                    target.attack(self, self.weapon, self.direction)
                    # self.player_grunt_channel.play(self.player_grunt)

        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        self.prev_direction = self.direction
        if self.velocity.x == 0:
            self.direction = self.prev_direction
        else:
            self.direction = math.copysign(1, self.velocity.x)
        self.weapon.update(delta, self.position, self.direction)

        if self.state == "RUN":
            frame = math.floor(self.current_frame)
            if self.velocity.x > 0:
                self.display = self.run_frames[math.floor(frame)]
                self.display_offsets["enemy"] = pg.Vector2(-60, -35)
            elif self.velocity.x <= 0:
                self.display = pg.transform.flip(self.run_frames[math.floor(frame)], True, False)
                self.display_offsets["enemy"] = pg.Vector2(-60, -35)
            if frame % 4 == 0 and self.on_ground:
                Dust(pg.Vector2(self.get_collision_rect().midbottom) + pg.Vector2(math.copysign(1, self.velocity.x) * -self.width/2,-15), 16, self.direction)
            self.current_frame = (self.current_frame + 0.25) % self.run_gif.n_frames
        elif self.state == "ATTACK":
            frame = math.floor(self.current_frame)
            if self.direction == 1:
                self.display = pg.transform.flip(self.attack_frames[math.floor(frame)], False, False)
                self.display_offsets["enemy"] = pg.Vector2(-60, -35)
            else:
                self.display = pg.transform.flip(self.attack_frames[math.floor(frame)], True, False)
                self.display_offsets["enemy"] = pg.Vector2(-60, -35)
            self.current_frame += 0.4
            if math.floor(self.current_frame) >= self.attack_gif.n_frames-1:
                self.state = "RUN"
                self.current_frame = 0

        # print(self.velocity)

    def knockout(self, node):
        self.stun_time = 100
        self.modify_health(-25, None)
        node.on_ground = False
        node.push(math.copysign(1, node.velocity.x), 0.25, -2.25)
        # self.crouch(1000)

    def draw(self, surf):
        # self.weapon.draw(surf)
        # super(Skeleton, self).draw(surf)
        surf.blit(self.display, get_display_rect(self.get_collision_rect()).topleft + self.display_offsets["enemy"])

        # for b in self.buffer:
        #     pg.draw.rect(surf,(0,0,255),get_display_rect(b),3)
        # self.buffer.append(self.get_collision_rect())
        # pg.draw.rect(surf, (0, 255, 0), get_display_rect(self.get_collision_rect()), 2)
class King(Actor):
    width, height = Actor.width * 2, Actor.height * 2
    speed = Actor.speed * 0.4
    jump_strength = Actor.jump_strength * 1.1
    colour = (235, 64, 52)
    friction = 0.5
    run_gif = Image.open("Assets/skeleton/skeleton_king_idle.gif")
    run_frames = []
    for i in range(run_gif.n_frames):
        run_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(run_gif, i)), (120, 180)))

    attack_gif = Image.open("Assets/skeleton/skeleton_king_summon.gif")
    attack_frames = []
    for i in range(attack_gif.n_frames):
        attack_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(attack_gif, i)), (120, 180)))
    # player_grunt = pg.mixer.Sound("Assets/SFX/Player Grunt.wav")
    # player_grunt_channel = pg.mixer.Channel(4)

    def __init__(self, pos, collision_layer, collision_mask, arrow_info):
        super().__init__(pos, collision_layer, collision_mask)

        self.areas = {
            "head": Area(self.position, pg.Vector2(self.width * 1 / 3 * 1 / 2, -2), self.width * 2 / 3, 25, Player,
                         self.knockout)}
        self.movable = False

        self.direction = -1
        self.prev_direction = self.direction

        self.health = 1 # for debugging without getting killed

        self.weapon = Lightning(self.position, (-125 - self.width/2,0), self.width, -1)
        self.buffer = []

        self.attack_cooldown = random.randint(2,5) * 1000

        self.display_offsets = {"enemy":pg.Vector2(0,0)}

        self.current_frame = 0
        self.display = self.run_frames[math.floor(self.current_frame)]
        self.state = "RUN"
        self.arrow_collision_mask, self.arrow_collision_layer = arrow_info
        self.ranged_attack = []

        self.skeleton_attack = False;

    def update(self, delta, target=None):
        super().update(delta)
        self.attack_cooldown -= delta
        self.attack_cooldown = max(0, self.attack_cooldown)
        if self.attack_cooldown == 0 and not self.attacked and target is not None and self.stun_time == 0 and not target.attacked:
            # self.follow_target(target, follow_range=750,stop_dist=target.width/2+self.weapon.width)
            # if get_display_rect(self.weapon.get_collision_rect()).colliderect(
            #         get_display_rect(target.get_collision_rect())):
            if self.state != "ATTACK":
                self.state = "ATTACK"
                self.current_frame = 0
                self.attack_cooldown = random.randint(2,5) * 1000

            if not get_display_rect(self.weapon.get_collision_rect()).colliderect(
                    get_display_rect(target.get_collision_rect())) and (1500 ** 2 > (self.position - target.position).length_squared()):


                if (self.position - target.position).length_squared() > 750 ** 2:
                    self.ranged_attack.append(RangedAttack(target.position + pg.Vector2(0,-250),self.arrow_collision_mask, self.arrow_collision_layer))
                    self.attack_cooldown = random.randint(5,10) * 1000
                else:
                    self.skeleton_attack = True
                    self.attack_cooldown = random.randint(5,10) * 1000


            # else:
            #     if self.state != "SUMMON":
            #         self.state = "SUMMON"
            #         self.current_frame = 0
            #         self.attack_cooldown = random.randint(2,5) * 1000
        if (self.state == "ATTACK") and (4 < self.current_frame) and (not self.attacked) and not target.attacked:
            if get_display_rect(self.weapon.get_collision_rect()).colliderect(
                    get_display_rect(target.get_collision_rect())):
                target.attack(self, self.weapon, math.copysign(1, target.position.x - self.position.x))
            # else:
            # # if (self.position - target.position).length_squared() > 750 ** 2:
            #     print('ranged')


        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        self.prev_direction = self.direction
        if self.velocity.x == 0:
            self.direction = self.prev_direction
        else:
            self.direction = math.copysign(1, self.velocity.x)
        self.weapon.update(delta, self.position, self.direction)
        for atk in self.ranged_attack:
            atk.update(delta)

        if self.state == "RUN":
            frame = math.floor(self.current_frame)
            self.display = self.run_frames[math.floor(frame)]
            self.display_offsets["enemy"] = pg.Vector2(-10, 25)
            self.current_frame = (self.current_frame + 0.025) % self.run_gif.n_frames

        elif self.state == "ATTACK":
            frame = math.floor(self.current_frame)
            if self.direction == 1:
                self.display = pg.transform.flip(self.attack_frames[math.floor(frame)], False, False)
                self.display_offsets["enemy"] = pg.Vector2(-15, -5)
            else:
                self.display = pg.transform.flip(self.attack_frames[math.floor(frame)], True, False)
                self.display_offsets["enemy"] = pg.Vector2(-15, 25)
            self.current_frame += 0.2
            if math.floor(self.current_frame) >= self.attack_gif.n_frames-1:
                self.state = "RUN"
                self.current_frame = 0
        # elif self.state == "SUMMON":
        #     frame = math.floor(self.current_frame)
        #     self.display = self.run_frames[math.floor(frame)]
        #     self.display_offsets["enemy"] = pg.Vector2(0, -35)
        #     self.current_frame = (self.current_frame + 0.025)
        #     if math.floor(self.current_frame) >= self.attack_gif.n_frames-1:
        #         self.state = "RUN"
        #         self.current_frame = 0

        # print(self.velocity)

    def knockout(self, node):
        self.stun_time = 100
        self.modify_health(-25, None)
        node.on_ground = False
        node.push(math.copysign(1, node.velocity.x), 0.25, -2.25)
        # self.crouch(1000)

    def draw(self, surf):
        # self.weapon.draw(surf)
        # super(King, self).draw(surf)
        surf.blit(self.display, get_display_rect(self.get_collision_rect()).topleft + self.display_offsets["enemy"])
        for atk in self.ranged_attack:
            atk.draw(surf)
        # for b in self.buffer:
        #     pg.draw.rect(surf,(0,0,255),get_display_rect(b),3)
        # self.buffer.append(self.get_collision_rect())
        # pg.draw.rect(surf, (0, 255, 0), get_display_rect(self.weapon.get_collision_rect()), 2)
