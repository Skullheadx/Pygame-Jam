from Setup import *

class fade:
    def __init__(self):
        self.transparency = 255
        self.overlay = pg.Surface((1080, 640))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(self.transparency)

    def update(self, transition = False):
        if self.transparency > 0 and not transition:
            self.transparency -= 3
            self.overlay.set_alpha(self.transparency)
        if self.transparency < 255 and transition:
            self.transparency += 3
            self.overlay.set_alpha(self.transparency)
    
    def draw(self):
        screen.blit(self.overlay, (0, 0))
class fadein:
    def __init__(self):
        self.transparency = 255
        self.overlay = pg.Surface((1080, 640))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(self.transparency)

    def update(self):
        if self.transparency > 0:
            self.transparency -= 3
            self.overlay.set_alpha(self.transparency)
            self.draw()
    
    def draw(self):
        screen.blit(self.overlay, (0, 0))


class fadeout:
    def __init__(self):
        self.transparency = 0
        self.overlay = pg.Surface((1080, 640))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(self.transparency)

    def update(self):
        if self.transparency < 255:
            self.transparency += 3
            self.overlay.set_alpha(self.transparency)
            self.draw()
            
    def draw(self):
        screen.blit(self.overlay, (0, 0))