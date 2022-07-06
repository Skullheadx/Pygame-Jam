from Setup import *
from Player import Player
from Block import Block

class Game:

    def __init__(self):
        self.collision_layer = {0:set(),1: set()}
        self.player = Player(center, self.collision_layer[1], self.collision_layer[0])
        self.blocks = [Block((SCREEN_WIDTH/2, SCREEN_HEIGHT * 3 / 4),self.collision_layer[0])]

    def update(self, delta):
        self.player.update(delta)
        for block in self.blocks:
            block.update(delta)

    def draw(self, surf):
        screen.fill((255, 255, 255))
        for block in self.blocks:
            block.draw(surf)

        self.player.draw(surf)
