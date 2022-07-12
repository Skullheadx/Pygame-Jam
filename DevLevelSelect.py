from Setup import *
from CommonImports.colours import black
from Function.createText import createText

from Game import Game
from Test import Test
from LevelCreator import LevelCreator
from MainMenu import Menu
import os.path

class DevLevelSelect:

    def __init__(self):
        self.texts = []
        X = 250
        self.texts.append(createText(X, 100, 32, black, "Bold", "DEVELOPER LEVEL SELECT",))
        self.texts.append(createText(X, 250, 24, black, "Regular", "MainMenu"))
        self.texts.append(createText(X, 350, 24, black, "Regular", "Game"))
        self.texts.append(createText(X, 450, 24, black, "Regular", "LevelCreator"))
        self.texts.append(createText(X, 550, 24, black, "Regular", "AutoLoad [-]"))

        self.texts.append(createText(X, 750, 24, black, "Regular", "Transition"))


        self.autoload = False

        if os.path.isfile('./Save/ignore_DevAutoload.txt'):
            global lines
            f = open("./Save/ignore_DevAutoload.txt", "r")
            lines = f.readlines()
            f.close()
        else:
            f = open("./Save/ignore_DevAutoload.txt", "x")
            f.close()

        try:
            self.level = int(lines[0])
        except:
            self.level = -3
        
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
            case 1:
                self.level = 0
            case 2:
                self.level = 1
            case 3:
                self.level = -2
            case 4:
                if(self.autoload == False):
                    self.texts[4] = createText(250, 550, 24, black, "Regular", "AutoLoad [x]")
                    self.autoload = True
                else:
                    self.texts[4] = createText(250, 550, 24, black, "Regular", "AutoLoad [-]")
                    self.autoload = False
                return;
            case 5:
                self.level = -4

        if(self.autoload == True):
            try:
                f = open("./Save/ignore_DevAutoload.txt", "x")
            except:
                f = open("./Save/ignore_DevAutoload.txt", "w")
            f.write(str(self.level))
            f.close()
