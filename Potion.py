from Setup import *
import threading

class Potion:
    
    def __init__(self, player, heal_amount = 25):
        self.heal = heal_amount
        self.player = player

    def get_input(self, player):
        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_1] and player.potion_cooldown == 0:
            self.consume_potion(player)
    
    def consume_potion(self, player):
        player.health += self.heal
        if player.health > 100:
            player.health = 100
            
        del self.player.potion_bag[0]
        self.player.potion_cooldown = 4
        threading.Thread(target = self.player.potion_cooldown_timer).start()
