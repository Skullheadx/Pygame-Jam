import Setup
from Setup import *
from Setup import camera_offset
from Player import Player
from Pet import Pet
from Enemy import Enemy
from Block import Block
from PhysicsBody import PhysicsBody
from World import World
from EndScreen import EndScreen
from UI.DashMeter import DashMeter


class Game:

    def __init__(self):
        self.collision_layer = {"none":set(),"world": set(), "player": set(), "enemy": set(), "pet": set()}

        self.player = Player(center, self.collision_layer["player"],
                             [self.collision_layer["enemy"], self.collision_layer["world"]],
                             [self.collision_layer["enemy"]])
        # self.pet = Pet(center, self.collision_layer["pet"], [self.collision_layer["world"]])

        self.world = World(self.collision_layer)

        self.enemies = [Enemy((SCREEN_WIDTH *3/ 4, SCREEN_HEIGHT / 2), self.collision_layer["enemy"],
                              [self.collision_layer["player"], self.collision_layer["world"]])]


        self.scene = EndScreen()
        self.dashMeter = DashMeter()
        self.level = 1
        self.scene.level = self.level

    def update(self, delta):
        Setup.camera_offset = self.player.update(delta)
        if self.player.dead:
            self.level = self.scene.level

        for i, enemy in enumerate(self.enemies):
            enemy.update(delta, self.player)
            if enemy.dead:
                self.enemies[i] = PhysicsBody(enemy.position, enemy.velocity, enemy.width, enemy.height, enemy.colour,
                                              enemy.collision_layer, enemy.collision_mask)
                self.collision_layer["enemy"].remove(enemy)
                self.collision_layer["enemy"].add(self.enemies[i])

        self.world.update(delta)

        # self.pet.update(delta, self.player, self.camera_pos)

    def draw(self, surf):
        screen.fill((255, 255, 255))
        self.world.draw(surf)
        for enemy in self.enemies:
            enemy.draw(surf)


        self.player.draw(surf)
        self.dashMeter.update(self.player.lastDash, self.player.dashCooldown)
        self.dashMeter.draw(surf)
        
        if self.player.dead:
            self.scene.update()
            self.scene.draw()
        
        

        # Debug Lines. DO NOT CROSS THEM!
        pg.draw.line(surf, (255, 0, 0), -Setup.camera_offset, pg.Vector2(SCREEN_WIDTH, -Setup.camera_offset.y), 10)
        pg.draw.line(surf, (255, 0, 0), -Setup.camera_offset, pg.Vector2(-Setup.camera_offset.x, SCREEN_HEIGHT), 10)
        # self.pet.draw(surf)
