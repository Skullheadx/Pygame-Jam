import Setup
from Setup import *
from CommonImports.colours import black
from Function.createText import createText
from Save.SaveGame import SaveGame

class EndScreen:

    def __init__(self, level=-1):
        self.texts = []
        X = SCREEN_WIDTH
        Y = SCREEN_HEIGHT/2
        self.texts.append(createText(X, Y, 32, black, "Bold", "You Died", 'c'))
        self.texts.append(createText(X, Y+150, 24, black, "Regular", "Respawn", 'c'))
        self.texts.append(createText(X, Y+300, 24, black, "Regular", "Save and Exit", 'c'))

        self.level = level

        
    def update(self):
        for ev in pg.event.get(pg.MOUSEBUTTONDOWN): # only track this event
            if ev.type == pg.MOUSEBUTTONDOWN: # dont need this line
                mouseX, mouseY = pg.mouse.get_pos()
                for i in range(len(self.texts)):
                    x1 = self.texts[i][1][0]
                    y1 = self.texts[i][1][1]
                    x2 = x1 + self.texts[i][0].get_rect()[2]
                    y2 = y1 + self.texts[i][0].get_rect()[3]

                    if (x1 <= mouseX <= x2 and y1 <= mouseY <= y2):
                        self.menuFunctions(i)
            return

    def draw(self):
        screen.fill((255, 255, 255))
        for i in self.texts:
            screen.blit(i[0], i[1])

    def menuFunctions(self, num):
        match num:
            case 1:
                self.level = -1
            case 2:
                SaveGame(self.level)
                self.level = 0
                # pg.quit();
