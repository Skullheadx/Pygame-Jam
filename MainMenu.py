from Setup import *
from CommonImports.colours import black
from Function.createText import createText

class Menu:

    def __init__(self):
        self.texts = []
        X = SCREEN_WIDTH
        Y = SCREEN_HEIGHT/2 - 100
        self.texts.append(createText(X, Y, 48, black, "Bold", "Interstellar Pirate Title", "c"))
        self.texts.append(createText(X, Y+200, 32, black, "Regular", "Start", "c"))
        self.texts.append(createText(X, Y+350, 32, black, "Regular", "Options", "c"))
        self.texts.append(createText(X, Y+500, 32, black, "Regular", "Quit", "c"))

        self.level = 0

        
    def update(self, delta):
        for ev in pg.event.get(pg.MOUSEBUTTONDOWN):
            if ev.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                for i in range(len(self.texts)):
                    x1 = self.texts[i][1][0]
                    y1 = self.texts[i][1][1]
                    x2 = x1 + self.texts[i][0].get_rect()[2]
                    y2 = y1 + self.texts[i][0].get_rect()[3]

                    if (x1 <= mouseX <= x2 and y1 <= mouseY <= y2):
                        self.menuFunctions(i)
            return

    def draw(self, surf):
        screen.fill((255, 255, 255))
        for i in self.texts:
            screen.blit(i[0], i[1])

    def menuFunctions(self, num):
        match num:
            case 1:
                self.level = self.level + 1
            case 2:
                print("Options")
            case 3:
                pg.quit();
