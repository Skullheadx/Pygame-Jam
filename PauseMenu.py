from Setup import *
from Function.createText import createText
import time
from Save.SaveGame import SaveGame

class PauseMenu:

    def __init__(self, level):
        X = SCREEN_WIDTH
        Y = SCREEN_HEIGHT/2

        self.subtitle = createText(X, Y - 150, 60, (255, 255, 255), "Regular", "Pause Menu", 'c')
        self.resume = createText(X, Y + 100, 30, (255, 255, 255), "Regular", "Resume", 'c')
        self.main_menu = createText(X, Y + 200, 30, (255, 255, 255), "Regular", "Main Menu", 'c')
        self.quit = createText(X, Y + 300, 30, (255, 255, 255), "Regular", "Quit", 'c')
        self.overlay = pg.Surface((1080, 640))
        self.overlay.fill((0, 0 ,0))
        self.overlay.set_alpha(127)

        self.level = level


    def update(self, game):
        for event in pg.event.get((pg.KEYUP,pg.MOUSEBUTTONUP)):
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                game.paused = False
                
            if event.type == pg.MOUSEBUTTONUP:
                mouse_loc = pg.mouse.get_pos()
                if self.resume[1].collidepoint(mouse_loc):
                    game.paused = False
                if self.main_menu[1].collidepoint(mouse_loc):
                    SaveGame(self.level)
                    self.level = 0
                if self.quit[1].collidepoint(mouse_loc):
                    pg.quit()
            return

    def draw(self):
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.subtitle[0], self.subtitle[1])
        screen.blit(self.resume[0], self.resume[1])
        screen.blit(self.main_menu[0], self.main_menu[1])
        screen.blit(self.quit[0], self.quit[1])
