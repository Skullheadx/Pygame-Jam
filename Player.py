from Setup import *

class Player:
    def __init__(self, pos):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(1,0)
    
    def update(self, delta):
        self.position += self.velocity

    # def move_and_collide(pos, vel):

    def draw(self, surf):
        pg.draw.circle(surf, (255,0,0), self.position, 10)
    