from abc import get_cache_token
from regex import D
from Function.WorldCoords import getWorldCoords
from Setup import *
from CommonImports.colours import white, black
from Function.createText import createText
from datetime import datetime, timedelta

class DialogueUI:

    def __init__(self):
        self.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet commodo leo."
        self.old_text = ""
        self.char = 0

        self.IDS = []
        self.dialogue_list = []
        self.PSA = 0
        self.lastTextTime = datetime.utcnow()

        self.skip = False
        self.texts = []

        self.drawText = []

    def update(self):
        return;

    def draw(self, surf, agent, text, sec, ID, Xt=-10000, Yt=-10000):

        if(not ID in self.IDS):
            temp = []
            c = []
            self.PSA += sec
            temp.append(text)
            temp.append(self.PSA)
            c.append(Xt)
            c.append(Yt)
            temp.append(c)
            self.IDS.append(ID)
            self.dialogue_list.append(temp)

        try:
            X, Y = 0, 0
            if(self.dialogue_list[self.char][2][0] == -10000 and self.dialogue_list[self.char][2][1] == -10000):
                X = get_display_point(agent.position)[0] + agent.width / 2
                Y = get_display_point(agent.position)[1]
            else:
                X, Y = get_display_point((self.dialogue_list[self.char][2][0], self.dialogue_list[self.char][2][1]))

                # print(get_display_point((X, Y)))
                print(get_camera_offset()[0] + SCREEN_WIDTH/2, get_camera_offset()[1] + SCREEN_HEIGHT/2)
            
            self.text = self.dialogue_list[self.char][0]
            self.checkTime()
            self.createDialogue()

            for i in range(len(self.drawText)):
                j = len(self.drawText) - i
                text_rect = self.drawText[i].get_rect(center=(X, Y-(20*j)))
                surf.blit(self.drawText[i], text_rect)
        except:
            pass;
    
    def createDialogue(self):
        if(self.text == self.old_text):
            self.skip == True
        else:
            self.old_text == self.text
            self.texts = []
            self.drawText = []
            self.skip == False

        if(self.skip == False):
            iii = 0
            while iii < len(self.text):
                n = 30
                if iii+n < len(self.text):
                    self.texts.append(self.text[iii:iii+n])
                else:
                    self.texts.append(self.text[iii:len(self.text)])
                iii += n

            for i in range(len(self.texts) - 1):
                text = self.texts[i].split(" ")[-1]
                self.texts[i+1] = self.texts[i][len(self.texts[i]) - len(text):] + self.texts[i+1]
                self.texts[i] = self.texts[i][:len(self.texts[i]) - len(text) - 1]

        for i in range(len(self.texts)):
            self.drawText.append(createText(0, 0, 20, white, "Regular", self.texts[i])[0])

        return;

    def checkTime(self):
        if(datetime.utcnow() - self.lastTextTime >= timedelta(seconds=self.dialogue_list[self.char][1])):
            if(self.char +1 < len(self.dialogue_list)):
                self.char = self.char + 1
            else:
                self.char = 0
                self.dialogue_list = []