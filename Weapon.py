from Setup import *


class Melee:
    img = pg.image.load("Assets/SWORD.png")
    def __init__(self, pos, offset, width,direction):
        self.position = pg.Vector2(pos)
        self.offset = pg.Vector2(offset)
        self.holder_width = width


    def update(self, delta):
        pass

    def draw(self, surf):
        pass
