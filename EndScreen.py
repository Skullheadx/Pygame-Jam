from Setup import *
from CommonImports.colours import black
from Function.createText import createText

class EndScreen:

    def __init__(self):
        self.texts = []
        X = 250
        self.texts.append(createText(X, 100, 32, black, "Bold", "You Died",))
        self.texts.append(createText(X, 250, 24, black, "Regular", "Respawn"))
        self.texts.append(createText(X, 350, 24, black, "Regular", "Options"))
        self.texts.append(createText(X, 450, 24, black, "Regular", "Quit"))

        self.level = -1

        
    def update(self):
        for ev in pg.event.get():
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

    def draw(self):
        screen.fill((255, 255, 255))
        for i in self.texts:
            screen.blit(i[0], i[1])

    def menuFunctions(self, num):
        match num:
            case 1:
                self.level = -1
            case 2:
                print("Options")
            case 3:
                pg.quit();
