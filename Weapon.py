import random

from Setup import *


class Melee:
    img = pg.transform.scale(pg.image.load("Assets/SWORD.png"), (40,40))
    flipped_img = pg.transform.flip(img,True,False)
    width,height = img.get_size()

    def __init__(self, pos, offset, pivot, width,direction):
        self.position = pg.Vector2(pos)
        self.offset = pg.Vector2(offset)
        self.pivot = self.position + pg.Vector2(pivot)
        self.holder_width = width

        self.direction = direction

        self.display = self.img
        self.display_rect = self.display.get_rect()
        self.swing_timer = 0


    def update(self, delta, pos, direction):
        self.position = pg.Vector2(pos)
        self.pivot = self.position + self.offset + pg.Vector2(self.width/2, self.height/2)
        self.direction = direction

        if self.direction == -1:
            angle = 25 * (math.sin(math.radians(self.swing_timer)))
            self.display, self.display_rect = rotate(self.position + self.offset, self.img, angle,self.pivot)
        elif self.direction == 1:
            angle = -25 * (math.sin(math.radians(self.swing_timer)))
            self.display, self.display_rect = rotate(self.position+ pg.Vector2(self.holder_width,0) + pg.Vector2(-self.offset.x, self.offset.y), self.flipped_img, angle,self.pivot + pg.Vector2(self.holder_width,0))

        self.swing_timer -= delta
        self.swing_timer = max(self.swing_timer, 0)

    def get_collision_rect(self):
        if self.direction == -1:
            return pg.Rect(self.display_rect.topleft,(self.width, self.height))
        elif self.direction == 1:
            return pg.Rect(self.display_rect.topleft,(self.width, self.height))

    def swing(self):
        if True:
            if self.swing_timer == 0:
                self.swing_timer = 360

    def draw(self, surf):
        surf.blit(self.display, get_display_rect(self.get_collision_rect()).topleft)
        # pygame.draw.circle(surf,(255,0,255),self.pivot,3)
        # pygame.draw.circle(surf,(0,255,0),self.position,3)
