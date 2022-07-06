from Setup import *


class Melee:
    img = pg.transform.smoothscale(pg.image.load("Assets/SWORD.png"), (40,40))
    flipped_img = pg.transform.flip(img,True,False)
    width,height = img.get_size()
    def __init__(self, pos, offset, width,direction):
        self.position = pg.Vector2(pos)
        self.offset = pg.Vector2(offset)
        self.holder_width = width


    def update(self, delta, pos, direction):
        self.position = pg.Vector2(pos)
        self.direction = direction

    def get_collision_rect(self):
        if self.direction == -1:
            return pg.Rect(self.position - pg.Vector2(self.width,0),(self.width, self.height))
        elif self.direction == 1:
            return pg.Rect(self.position + pg.Vector2(self.holder_width,0),(self.width, self.height))

    def draw(self, surf):
        if self.direction == -1:
            surf.blit(self.img, self.get_collision_rect().topleft)
        else:
            surf.blit(self.flipped_img, self.get_collision_rect().topleft)
