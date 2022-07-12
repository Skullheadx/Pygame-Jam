from re import T

from regex import F

import Setup
from Block import Block
from EndScreen import EndScreen
from Enemy import Enemy
from Function.Fade import fade
from Function.Portal import Transition
from Pet import Pet
from PhysicsBody import PhysicsBody
from Player import Player
from Setup import *
from Setup import camera_offset
from UI.DashMeter import DashMeter
from UI.Dialogue import DialogueUI
from UI.HealthBar import HealthBar
from UI.PotionUI import PotionUI
from World import World
from Item import PotionItem


class Game:

    def __init__(self, level):
        self.collision_layer = {"none": set(), "world": set(), "player": set(), "enemy": set(), "pet": set(), "body":set(), "potion":set()}

        # self.load_world(level)

        self.sky = pg.image.load("Assets/world/VOID.png").convert()


        self.world = World(self.collision_layer)

        enemy_positions, player_position, self.portal_position, heal_positions = self.world.load_world(level)

        for i in heal_positions:
            PotionItem(i, self.collision_layer["potion"])

        self.player = Player(player_position, self.collision_layer["player"],
                             [self.collision_layer["enemy"], self.collision_layer["world"]],
                             [self.collision_layer["enemy"], self.collision_layer["body"]],
                             self.collision_layer["potion"])
        # self.pet = Pet(center, self.collision_layer["pet"], [self.collision_layer["world"]])
        self.enemies = [Enemy(pos, self.collision_layer["enemy"],
                              [self.collision_layer["player"], self.collision_layer["world"]]) for pos in
                        enemy_positions]
        self.scene = EndScreen()
        # self.dashMeter = DashMeter(self.player.dashCooldown)
        self.healthBar = HealthBar()
        self.potionUI = PotionUI()
        self.level = level
        self.scene.level = self.level

        self.Transition = Transition()
        self.fade = self.Transition.fade
        self.fadeT = fade()
        self.next_level = 0

        self.dialogue = DialogueUI()

    # def load_world(self, level):

    def update(self, delta):
        Setup.camera_offset = self.player.update(delta)
        Setup.camera_offset.x = max(0, min(Setup.camera_offset.x, MAP_WIDTH - SCREEN_WIDTH))
        Setup.camera_offset.y = max(0, min(Setup.camera_offset.y, MAP_HEIGHT - SCREEN_HEIGHT))
        if self.player.dead:
            self.level = self.scene.level

        for i, enemy in enumerate(self.enemies):
            enemy.update(delta, self.player)
            if enemy.dead:
                self.enemies[i] = PhysicsBody(enemy.position, enemy.velocity, enemy.width, enemy.height, enemy.colour,
                                              self.collision_layer["body"], [self.collision_layer["world"], self.collision_layer["body"]])
                self.collision_layer["enemy"].remove(enemy)
                self.collision_layer["body"].add(self.enemies[i])

        for particle in particles:
            particle.update(delta)

        self.world.update(delta)
        self.fade = self.Transition.fade

        # self.pet.update(delta, self.player, self.camera_pos)

    def draw(self, surf):
        # screen.fill((0, 191, 255))

        # screen.fill((0, 191, 255))
        # screen.fill((255,255,255))
        surf.blit(self.sky,(0,0))

        if (self.level == 1):
            self.dialogue.draw(surf, self.enemies[0], "enemy dialogue")
            self.dialogue.draw(surf, self.player, "player dialogue")

        try:
            self.Transition.draw(surf, self.player.position, self.portal_position)
        except:
            pass;

        self.world.draw(surf)

        for potion in self.collision_layer["potion"]:
            potion.draw(surf)

        for particle in particles:
            particle.draw(surf)

        for enemy in self.enemies:
            enemy.draw(surf)


        self.player.draw(surf)
        # self.dashMeter.update(self.player.lastDash)
        # self.dashMeter.draw(surf)
        self.healthBar.draw(surf, self.player.health)
        self.potionUI.draw(surf, self.player.potion_bag, self.player.potion_cooldown)            

        # print(self.player.get_collision_rect())s
        # Debug Lines. DO NOT CROSS THEM!
        pg.draw.line(surf, (255, 0, 0), -Setup.camera_offset, pg.Vector2(SCREEN_WIDTH, -Setup.camera_offset.y), 10)
        pg.draw.line(surf, (255, 0, 0), -Setup.camera_offset, pg.Vector2(-Setup.camera_offset.x, SCREEN_HEIGHT), 10)
        # self.pet.draw(surf)

        if(self.fade == True):
            self.fadeT.update(True)
            self.fadeT.draw()
        else:
            self.fadeT.update()
            self.fadeT.draw()

        if(self.fadeT.transparency >= 255):
            self.Transition.fade = False
            self.next_level = self.level + 1
            self.level = -4

        if self.player.dead:
            self.scene.update()
            self.scene.draw()
