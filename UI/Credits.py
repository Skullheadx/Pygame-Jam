import Setup
from Setup import *
from CommonImports.colours import black, red
from Function.createText import createText

class Credits:

    def __init__(self):
        self.texts = []
        X = SCREEN_WIDTH
        Y = SCREEN_HEIGHT/4 
        
        # CHANGE YOUR NAME HERE IF YOU WANT
        self.texts.append(createText(X, Y+800, 24, black, "Regular", "Exit", "c"))

        self.texts.append(createText(X, Y-40, 48, black, "Bold", "Credits:", "c"))
        self.texts.append(createText(X, Y+40, 30, red, "SemiBold", "FAILURE Studios", "c"))

        self.texts.append(createText(X - 400, Y+200, 32, black, "Regular", "Programmers:", "c"))
        self.texts.append(createText(X - 400, Y+300, 24, black, "Regular", "Skullhead", "c"))
        self.texts.append(createText(X - 400, Y+400, 24, black, "Regular", "lbcmk", "c"))
        self.texts.append(createText(X - 400, Y+500, 24, black, "Regular", "Enlightened", "c"))
        
        self.texts.append(createText(X + 400, Y+200, 32, black, "Regular", "Artists:", "c"))
        self.texts.append(createText(X + 400, Y+300, 24, black, "Regular", "Landy", "c"))
        self.texts.append(createText(X + 400, Y+400, 24, black, "Regular", "MountainH", "c"))

        self.level = -5

        try:
            pg.mixer.music.load('Assets/Music/Main_Menu_Music.ogg')
            pg.mixer.music.play(-1)
        except:
            pass;
        
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
            case 0:
                self.level = 6
