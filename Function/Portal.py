from Setup import *
from CommonImports.colours import white
from Function.createText import createText
from Function.WorldCoords import *

class Transition:

    def __init__(self, nextLevel, X, Y):
        self.level = nextLevel
        self.x = X
        self.y = Y

        self.height = 150
        self.width = 80

        self.portal_stage = 0
        self.portalYAnim = 1
        self.down = False

        
    def update(self):
        return;

    def draw(self, surf, offsetX=0, offsetY=0):
        
        coords = getWorldCoords(0, 0)

        coords[1] += self.portalYAnim
        a = (((offsetX-self.width/2) + coords[0], offsetY + coords[1]), (offsetX+coords[0], offsetY-self.height/2+coords[1]), (offsetX+self.width/2 + coords[0], offsetY+coords[1]), (offsetX + coords[0], offsetY+self.height/2 + coords[1]))

        pg.draw.polygon(surf, (107, 18, 158), a)

        if(self.portalYAnim <= -25 and self.down == False):
            self.down = True
        elif(self.portalYAnim >= 0):
            self.down = False
        
        if(self.down == True):
            self.portalYAnim += 1
        else:
            self.portalYAnim -= 1
