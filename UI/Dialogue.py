from Setup import *
from CommonImports.colours import white, black
from Function.createText import createText

class DialogueUI:

    def __init__(self):
        self.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet commodo leo."
        self.old_text = ""
        self.char = 0

        self.skip = False
        self.texts = []

        self.drawText = []

    def update(self):
        return;

    def draw(self, surf, agent, text):
        
        X = get_display_point(agent.position)[0] + agent.width / 2
        Y = get_display_point(agent.position)[1]
        self.text = text
        self.createDialogue()

        for i in range(len(self.drawText)):
            j = len(self.drawText) - i
            text_rect = self.drawText[i].get_rect(center=(X, Y-(20*j)))
            surf.blit(self.drawText[i], text_rect)
    
    def createDialogue(self):
        if(self.text == self.old_text):
            self.skip == True
        else:
            self.old_text == self.text
            self.texts = []
            self.drawText = []
            self.char = 0
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
            # if(self.char/30 > i):
            #     self.drawText.append(createText(0, 0, 30, white, "Regular", self.texts[i])[0])
            # else:
            #     self.drawText.append(createText(0, 0, 30, white, "Regular", self.texts[i][self.char%30:])[0])
        # self.char += 1

        return;
