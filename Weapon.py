from Setup import *


class Melee:
    img = pg.transform.smoothscale(pg.image.load("Assets/SWORD.png"), (40,40))
    flipped_img = pg.transform.flip(img,True,False)
    width,height = img.get_size()
    def __init__(self, pos, offset, width,direction):
        self.position = pg.Vector2(pos)
        self.offset = pg.Vector2(offset)
        self.holder_width = width

        self.direction = direction

        self.display = self.img
        self.swing_timer = 0

    def update(self, delta, pos, direction):
        self.position = pg.Vector2(pos)
        self.direction = direction

        if self.direction == -1:
            self.display = pg.transform.rotate(self.img, 360 * math.sin(math.radians(self.swing_timer/10)))
        elif self.direction == 0:
            self.display = pg.transform.rotate(self.flipped_img, -360 * math.sin(math.radians(self.swing_timer/10)))

        self.swing_timer -= delta
        self.swing_timer = max(self.swing_timer, 0)

    def get_collision_rect(self):
        if self.direction == -1:
            return pg.Rect(self.position - pg.Vector2(self.width,0),(self.width, self.height))
        elif self.direction == 1:
            return pg.Rect(self.position + pg.Vector2(self.holder_width,0),(self.width, self.height))

    def swing(self):
        if self.swing_timer == 0:
            self.swing_timer = 1800

    def draw(self, surf):
        surf.blit(self.display, self.get_collision_rect().topleft)
