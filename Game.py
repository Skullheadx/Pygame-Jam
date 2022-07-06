from Setup import *
from Player import Player
from Pet import Pet
from Enemy import Enemy
from Block import Block

class Game:

    def __init__(self):
        self.collision_layer = {"world":set(),"player": set(), "enemy":set(), "pet":set()}

        self.player = Player(center, self.collision_layer["player"], [self.collision_layer["enemy"], self.collision_layer["world"]])
        self.pet = Pet(center, self.collision_layer["pet"], [self.collision_layer["world"]])

        self.enemies = [Enemy((SCREEN_WIDTH * 3 /4, 0),self.collision_layer["enemy"], [self.collision_layer["player"], self.collision_layer["world"]])]
        self.blocks = [Block((0, SCREEN_HEIGHT * 3 / 4),self.collision_layer["world"])]
                    #    Block((SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT * 3 / 4),self.collision_layer[0]),
                    #    Block((SCREEN_WIDTH/2 + 50, SCREEN_HEIGHT * 3 / 4),self.collision_layer[0]),


    def update(self, delta):
        self.player.update(delta)
        # self.pet.update(delta, self.player)

        for enemy in self.enemies:
            enemy.update(delta, self.player)

        for block in self.blocks:
            block.update(delta)
        
    def draw(self, surf):
        screen.fill((255, 255, 255))
        for enemy in self.enemies:
            enemy.draw(surf)
        for block in self.blocks:
            block.draw(surf)

        self.player.draw(surf)
        self.pet.draw(surf)
