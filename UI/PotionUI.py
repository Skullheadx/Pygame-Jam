from Setup import *
from Function.createText import createText
from CommonImports.colours import white


#Potion UI

class PotionUI:

    def __init__(self):
        self.X = 20
        self.Y = 70
        self.d = 35

        buttonImage = pg.image.load('./Assets/world/decor/HEALTHPOTION.png')
        self.potionImage= pg.transform.scale(buttonImage, (30, 30))

    def update(self):
        return;

    def draw(self, surf, potion_bag, potion_cooldown):
        #Amount of Potions Display
        # num_of_potions = createText(0, 0, 30, white, "Regular", str(len(potion_bag)) + " Potions")[0]
        for i in range(len(potion_bag)):
            potion_text_rect = self.potionImage.get_rect(left = 20+(self.d*i), top = 70)
            surf.blit(self.potionImage, potion_text_rect)

        #Cooldown Display
        if potion_cooldown > 0:
            potion_cd_ui = createText(0, 0, 20, white, "Regular", str(potion_cooldown) + "s potion cooldown")[0]
            potion_cd_rect = self.potionImage.get_rect(left = 20, top = 100)
            surf.blit(potion_cd_ui, potion_cd_rect)
