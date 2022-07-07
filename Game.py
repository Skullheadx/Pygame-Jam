import Setup
from Setup import *
from Setup import camera_offset
from Player import Player
from Pet import Pet
from Enemy import Enemy
from Block import Block
from PhysicsBody import PhysicsBody

class Game:

    def __init__(self):
        self.collision_layer = {"world":set(),"player": set(), "enemy":set(), "pet":set()}

        self.player = Player(center, self.collision_layer["player"], [self.collision_layer["enemy"], self.collision_layer["world"]])
        # self.pet = Pet(center, self.collision_layer["pet"], [self.collision_layer["world"]])

        self.enemies = [Enemy((SCREEN_WIDTH * 3 /4, 0),self.collision_layer["enemy"], [self.collision_layer["player"], self.collision_layer["world"]])]
        self.blocks = [Block((0, SCREEN_HEIGHT * 3 / 4),self.collision_layer["world"]),
                       Block((SCREEN_WIDTH, SCREEN_HEIGHT * 3 / 4 - 25),self.collision_layer["world"])]


    def update(self, delta):

        for i,enemy in enumerate(self.enemies):
            enemy.update(delta, self.player)
            if enemy.dead:
                self.enemies[i] = PhysicsBody(enemy.position,enemy.velocity,enemy.width,enemy.height,enemy.colour,enemy.collision_layer,enemy.collision_mask)
                self.collision_layer["enemy"].remove(enemy)
                self.collision_layer["enemy"].add(self.enemies[i])

        for block in self.blocks:
            block.update(delta)

        Setup.camera_offset += self.player.update(delta)

        # self.pet.update(delta, self.player, self.camera_pos)

    def draw(self, surf):
        screen.fill((255, 255, 255))
        for enemy in self.enemies:
            enemy.draw(surf)
        for block in self.blocks:
            block.draw(surf)

        self.player.draw(surf)
        # self.pet.draw(surf)
