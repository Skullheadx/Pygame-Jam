from Setup import *


class Object:

    def __init__(self, pos):
        self.position = pg.Vector2(pos)
        self.width,self.height = 0,0

    def update(self, delta):
        pass

    def draw(self, surf):
        pass
