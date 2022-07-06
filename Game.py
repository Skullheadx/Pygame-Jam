from Setup import *
from Player import Player
from Enemy import Enemy
from Block import Block

class Game:

    def __init__(self):
        self.collision_layer = {0:set(),1: set(), 2:set()}
        self.player = Player(center, self.collision_layer[1], [self.collision_layer[2], self.collision_layer[0]])
        self.enemies = [Enemy((SCREEN_WIDTH * 3 /4, 0),self.collision_layer[2], [self.collision_layer[1], self.collision_layer[0]])]
        self.blocks = [Block((0, SCREEN_HEIGHT * 3 / 4),self.collision_layer[0]),
                    #    Block((SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT * 3 / 4),self.collision_layer[0]),
                    #    Block((SCREEN_WIDTH/2 + 50, SCREEN_HEIGHT * 3 / 4),self.collision_layer[0]),

                       ]

    def update(self, delta):
        self.player.update(delta)
        for enemy in self.enemies:
            enemy.update(delta)
            enemy.follow_player(self.player)

        for block in self.blocks:
            block.update(delta)

    def draw(self, surf):
        screen.fill((255, 255, 255))
        for enemy in self.enemies:
            enemy.draw(surf)
        for block in self.blocks:
            block.draw(surf)

        self.player.draw(surf)
