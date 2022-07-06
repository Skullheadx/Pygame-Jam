from Setup import *


class Block:
    width, height = 50, 50
    colour = (71, 77, 97)

    def __init__(self, pos, collision_layer):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0,0) # So that we may have moving blocks
        collision_layer.add(self)

    def update(self, delta):
        pass # when player "moves", it's actually the blocks

    def get_collision_rect(self):
        return pg.Rect(self.position, (self.width, self.height))

    def draw(self, surf):
        pg.draw.rect(surf, self.colour, self.get_collision_rect(), border_radius=5)
