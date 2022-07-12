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
from Spike import Spike
from Particle import Cloud

class Game:
    cloud_density = 1/100000


    def __init__(self, level):
        self.collision_layer = {"none": set(), "world": set(), "player": set(), "enemy": set(), "pet": set(),
                                "body": set(), "potion": set(), "spike": set()}

        # self.load_world(level)

        self.levels = [[], [], [8, 9]]


        self.world = World(self.collision_layer)

        enemy_positions, player_position, self.portal_position, heal_positions, spike_positions = self.world.load_world(
            level)

        for i in heal_positions:
            PotionItem(i, self.collision_layer["potion"])
        for i in spike_positions:
            Spike(i, self.collision_layer["spike"])

        self.player = Player(player_position, self.collision_layer["player"],
                             [self.collision_layer["enemy"], self.collision_layer["world"]],
                             [self.collision_layer["enemy"], self.collision_layer["body"]],
                             self.collision_layer["potion"],
                             self.collision_layer["spike"])
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

        if self.level in [1,3,4]:
            # Density = total clouds / area
            # Total_clouds = area * density
            for i in range(round(MAP_WIDTH * SCREEN_HEIGHT * 2 / 3 * self.cloud_density)):
                Cloud((random.random() * MAP_WIDTH, random.random() * SCREEN_HEIGHT * 2 / 3), random.randint(100,125))

        self.sky = pg.image.load("Assets/world/sky_level_background.png").convert()

        try:
            if self.level == 1:
                pg.mixer.music.load("Assets/Music/Overworld_Music.ogg")
            if self.level == 2:
                pg.mixer.music.load("Assets/Music/Cave_Music.ogg")
                self.sky = pg.image.load("Assets/world/VOID.png").convert()

            if self.level == 3 or self.level == 4:
                pg.mixer.music.load("Assets/Music/Sky_Music.ogg")
            if self.level == 5:
                pg.mixer.music.load("Assets/Music/Combat_Music.ogg")
                self.sky = pg.image.load("Assets/world/VOID.png").convert()

            else:
                pg.mixer.music.load("Assets/Music/Overworld_Music.ogg")

            pg.mixer.music.play(-1)
        except:
            pass;

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
                                              self.collision_layer["body"],
                                              [self.collision_layer["world"], self.collision_layer["body"]])
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
        surf.blit(self.sky, (0, 0))

        if (self.player.position[1] > 10000):
            self.player.dead = True

        if (self.level in self.levels[2]):
            self.sky = pg.image.load("Assets/world/sky_level_background.png").convert()

        for particle in particles:
            particle.draw(surf)
        self.world.draw(surf)

        for potion in self.collision_layer["potion"]:
            potion.draw(surf)
        for spike in self.collision_layer["spike"]:
            spike.draw(surf)

        if (self.level == 1):
            self.dialogue.draw(surf, self.enemies[0], "enemy dialogue")
            self.dialogue.draw(surf, self.player, "player dialogue")

        try:
            self.Transition.draw(surf, self.player.position, self.portal_position)
        except:
            pass;

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

        if (self.fade == True):
            self.fadeT.update(True)
            self.fadeT.draw()
        else:
            self.fadeT.update()
            self.fadeT.draw()

        if (self.fadeT.transparency >= 255):
            self.Transition.fade = False
            self.next_level = self.level + 1
            self.level = -4

        if self.player.dead:
            self.scene.update()
            self.scene.draw()
