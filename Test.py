from Setup import *


class Test:

    def __init__(self):
        self.position = center.copy()

        self.angle = 0
        self.pivot = pg.Vector2(SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 2 + 50)
        self.img = pg.transform.scale(pygame.image.load("Assets/SWORD.png"), (100, 100))
        self.display = self.img.copy()
        self.img_rect = self.display.get_rect()

    def update(self, delta):
        self.display, self.img_rect = rotate(self.position, self.img, self.angle, self.pivot)

        self.angle += 1

    def draw(self, surf):
        surf.fill((0, 0, 0))
        surf.blit(self.display, self.img_rect.topleft)

        pg.draw.circle(surf, (255, 0, 0), self.pivot, 3)
