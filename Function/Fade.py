from Setup import *

class fadein:
    def __init__(self):
        self.transparency = 255
        self.overlay = pg.Surface((1080, 640))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(self.transparency)

    def update(self):
        if self.transparency > 0:
            self.transparency -= 1
            self.overlay.set_alpha(self.transparency)
            self.draw()
    
    def draw(self):
        screen.blit(self.overlay, (0, 0))


class fadeout():
    def __init__(self):
        self.transparency = 0
        self.overlay = pg.Surface((1080, 640))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(self.transparency)

    def update(self):
        if self.transparency < 255:
            self.transparency += 1
            self.overlay.set_alpha(self.transparency)
            self.draw()
            
    def draw(self):
        screen.blit(self.overlay, (0, 0))