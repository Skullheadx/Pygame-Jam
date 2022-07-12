from Setup import *


class Spike:
    width, height = 50, 50
    img = pg.transform.scale(pg.image.load("Assets/world/decor/SPIKE.png"), (50, 50))

    def __init__(self, pos, collision_layer):
        self.position = pg.Vector2(pos)
        collision_layer.add(self)

    def update(self, delta):
        pass

    def get_collision_rect(self):
        return pg.Rect(self.position, (self.width, self.height))

    def draw(self, surf):
        surf.blit(self.img, get_display_rect(self.get_collision_rect()))
