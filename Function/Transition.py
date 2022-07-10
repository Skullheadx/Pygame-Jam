from Setup import *
from random import randint, uniform
from datetime import datetime, timedelta
from CommonImports.colours import white
from Function.Fade import fade

class TransitionScene:

    char_frames = [
        pg.transform.scale(pg.image.load(path.join("Assets/player/idle", file)).subsurface(pg.Rect(179, 169, 170, 401)),
                           (50, 100)) for file in listdir("Assets/player/idle")]

    def __init__(self, next_level):
        self.level = -4
        self.next_level = next_level

        self.stars = []
        for i in range(100):
            self.stars.append([randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT), uniform(1, 2)])
        self.starLen = 0
        self.timeSinceStart = datetime.utcnow()

        # self.down = True
        self.frames = 0
        self.rotate_angle = 0
        # self.x = SCREEN_WIDTH/2 - 100
        self.x = 0
        self.y = SCREEN_HEIGHT/2 - 50

        self.x2 = self.x
        self.y2 = self.y

    def update(self, delta):
        # if(self.starLen <= 75):
        self.starLen += 0.5
        
        self.x = self.x + 7
        self.y = self.y - 0.3

        self.x2 = self.x + randint(-2, 2)
        self.y2 = self.y + randint(-2, 2)


        if(datetime.utcnow() - self.timeSinceStart > timedelta(seconds=3)):
            self.level = self.next_level


        if(self.rotate_angle < 360):
            self.rotate_angle += 1
        else:
            self.rotate_angle = 0

        if(self.frames+1 < len(self.char_frames)):
            self.frames += 1
        else: 
            self.frames = 0

    def draw(self, surf):
        surf.fill((0, 0, 0))
        if(self.starLen > 0):
            for i in range(len(self.stars)):
                pg.draw.line(surf, white, (self.stars[i][0], self.stars[i][1]), (self.stars[i][0] - (self.starLen*self.stars[i][2]), self.stars[i][1] + (self.starLen*self.stars[i][2]/15)))
        image = pg.transform.rotate(self.char_frames[self.frames], self.rotate_angle)
        surf.blit(image, (self.x2, self.y2))