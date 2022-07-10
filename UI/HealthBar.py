from Setup import *
from CommonImports.colours import white, red
from Function.createText import createText
from datetime import datetime

class HealthBar:

    def __init__(self):
        return;
        
    def update(self):
        return;

    def draw(self, surf, health):
        # Healthbar Stuff
        # bar is made of 2 rectanges, background which is just a simple rectange and foreground which goes on top and has a bit of math involved
        background_rect = pg.Rect(20, 20, 1080 * 0.2, 640 * 0.08)

        # idea is that 1080*0.185 = size of bar at 100% hp, at lower hp you want to get a fraction of that which is why we multiply by (health*0.01) example: 70 hp * 0.01 = 0.7
        foreground_rect = pg.Rect(0, 0, 1080 * 0.185 * (health * 0.01), 640 * 0.06)
        # make sure the red part health bar always sits on the left
        # sets bar to center of background bar, then subtracts 1/2 of blank space to put it on the left
        foreground_rect.center = (
            background_rect.centerx - 1080 * 0.185 * ((1 - health * 0.01) / 2), background_rect.centery)
        pg.draw.rect(surf, (54, 54, 54), background_rect)
        pg.draw.rect(surf, red, foreground_rect)

        # text
        current_health_display = createText(0, 0, 30, white, "Regular", str(health) + "/100")[0]
        text_rect = current_health_display.get_rect(center=background_rect.center)
        surf.blit(current_health_display, text_rect)