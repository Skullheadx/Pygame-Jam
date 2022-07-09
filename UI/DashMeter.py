from Setup import *
from CommonImports.colours import white
from Function.createText import createText
from datetime import datetime

class DashMeter:

    def __init__(self):
        self.texts = ['a']
        self.timeSinceLastDash = datetime.utcnow()
        self.timer = self.timeSinceLastDash.second + self.timeSinceLastDash.microsecond / 100000

        
    def update(self, dash, cooldown):
        self.timeSinceLastDash = datetime.utcnow() - dash
        self.timer = self.timeSinceLastDash.seconds + self.timeSinceLastDash.microseconds / 1000000
        if(self.timer > cooldown.seconds + cooldown.microseconds/1000000):
            self.timer = cooldown.seconds + cooldown.microseconds/1000000

    def draw(self, surf):
        background_rect = pg.Rect(844, 20, 1080 * 0.2, 640 * 0.08)
        foreground_rect = pg.Rect(0, 0, 1080 * 0.185 * (self.timer * 0.4), 640 * 0.06)
        self.texts[0] = createText(0, 0, 30, white, "Regular", str(round(self.timer/0.025)) + "%")[0]

        foreground_rect.center = (
            background_rect.centerx - 1080 * 0.185 * ((1 - self.timer * 0.4) / 2), background_rect.centery)

        pg.draw.rect(surf, (54, 54, 54), background_rect)
        pg.draw.rect(surf, (175, 175, 175), foreground_rect)

        text_rect = self.texts[0].get_rect(center=background_rect.center)
        surf.blit(self.texts[0], text_rect)
