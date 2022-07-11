from Setup import *
from CommonImports.colours import white
from Function.createText import createText
from Function.WorldCoords import *

class Transition:

    def __init__(self):
        self.height = 150
        self.width = 80

        self.portal_stage = 0
        self.portalYAnim = 1
        self.down = False

        self.buttonStage = 0
        buttonImage = pg.image.load('./Assets/buttons/e.png')
        self.buttonImage = pg.transform.scale(buttonImage, (self.width/2, self.width/2))

        self.fade = False

        
    def update(self):
        return;

    def draw(self, surf, playerPos, offset=(0,0)):
        offsetX = offset[0]
        offsetY = offset[1] - 25
        
        coords = getWorldCoords(0, 0)

        coords[1] += self.portalYAnim
        a = (((offsetX-self.width/2) + coords[0], offsetY + coords[1]), (offsetX+coords[0], offsetY-self.height/2+coords[1]), (offsetX+self.width/2 + coords[0], offsetY+coords[1]), (offsetX + coords[0], offsetY+self.height/2 + coords[1]))
        portal_rect = (a[0][0], a[1][1], a[2][0], a[3][1])
        # print(portal_rect)
        # print(playerPos[0], playerPos[1])

        print(portal_rect, coords, playerPos)
        
        if(a[0][0] < playerPos[0]+self.width/2 < a[2][0] and a[1][1] < playerPos[1] < a[3][1]):
            # self.buttonStage += 0.1
            surf.blit(self.buttonImage, (a[0][0]+self.width/4, a[1][1]-(2*self.width/3)))
            pressed = pg.key.get_pressed()
            if pressed[pg.K_e] or pressed[pg.K_RETURN]:
                self.fade = True;

        pg.draw.polygon(surf, (107, 18, 158), a)

        if(self.portalYAnim <= -25 and self.down == False):
            self.down = True
        elif(self.portalYAnim >= 0):
            self.down = False
        
        if(self.down == True):
            self.portalYAnim += 0.5
        else:
            self.portalYAnim -= 0.5
