from Setup import *
from CommonImports.colours import white
from Function.createText import createText
from Save.SaveGame import LoadGame

class Menu:

    def __init__(self):
        self.texts = []
        X = SCREEN_WIDTH
        Y = SCREEN_HEIGHT/2
        self.texts.append(createText(X, Y, 48, white, "Bold", "Interstellar Pirate Title", "c"))
        self.texts.append(createText(X, Y+200, 32, white, "Regular", "Start", "c"))
        self.texts.append(createText(X, Y+350, 32, white, "Regular", "New Game", "c"))
        self.texts.append(createText(X, Y+500, 32, white, "Regular", "Quit", "c"))

        backgroundImage = pg.image.load('./Assets/mainmenu_background.png')
        self.backgroundImage = pg.transform.scale(backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.level = 0

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
        # screen.fill((255, 255, 255))
        surf.blit(self.backgroundImage, (0, 0))
        for i in self.texts:
            screen.blit(i[0], i[1])

    def menuFunctions(self, num):
        match num:
            case 1:
                try:
                    self.level = LoadGame()
                    if(self.level == 0):
                        self.level = 1
                except:
                    self.level = self.level + 1
            case 2:
                self.level = 1
            case 3:
                pg.quit();
