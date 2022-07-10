from Setup import *
from Function.createText import createText
from CommonImports.colours import white


#Potion UI

class PotionUI:

    def __init__(self):
        return;

    def update(self):
        return;

    def draw(self, surf, potion_bag, potion_cooldown):
        #Amount of Potions Display
        num_of_potions = createText(0, 0, 30, white, "Regular", str(len(potion_bag)) + " Potions")[0]
        potion_text_rect = num_of_potions.get_rect(left = 20, top = 70)
        surf.blit(num_of_potions, potion_text_rect)

        #Cooldown Display
        if potion_cooldown > 0:
            potion_cd_ui = createText(0, 0, 30, white, "Regular", str(potion_cooldown) + " until potion can be used")[0]
            potion_cd_rect = num_of_potions.get_rect(left = 20, top = 100)
            surf.blit(potion_cd_ui, potion_cd_rect)
