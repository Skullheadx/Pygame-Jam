from Setup import *
from Player import Player

class Game:

    def __init__(self):
        self.player = Player(center)

    def update(self, delta):
        self.player.update(delta)

    def draw(self, surf):
        self.player.draw(surf)
