import Setup
from EndScreen import EndScreen
from Enemy import Enemy
from Function.Fade import fade
from Function.Portal import Transition
from Item import PotionItem
from Object import Object
from Particle import Cloud
from PauseMenu import PauseMenu
from PhysicsBody import PhysicsBody
from Player import Player
from Setup import *
from Spike import Spike
from UI.Dialogue import DialogueUI
from UI.HealthBar import HealthBar
from UI.PotionUI import PotionUI
from World import World


class Game:
    cloud_density = 1 / 100000

    def __init__(self, level):
        self.collision_layer = {"none": set(), "world": set(), "player": set(), "enemy": set(), "pet": set(),
                                "body": set(), "potion": set(), "spike": set()}

        # self.load_world(level)

        self.levels = [[], [], [3, 4]]

        self.world = World(self.collision_layer)

        enemy_positions, player_position, self.portal_position, heal_positions, spike_positions = self.world.load_world(
            level)

        for i in heal_positions:
            PotionItem(i, self.collision_layer["potion"])
        for i in spike_positions:
            Spike(i, self.collision_layer["spike"])

        self.player = Player(player_position, self.collision_layer["player"],
                             [self.collision_layer["enemy"], self.collision_layer["world"]],
                             [self.collision_layer["enemy"], self.collision_layer["body"]],
                             self.collision_layer["potion"],
                             self.collision_layer["spike"])
        # self.pet = Pet(center, self.collision_layer["pet"], [self.collision_layer["world"]])
        self.enemies = [Enemy(pos, self.collision_layer["enemy"],
                              [self.collision_layer["player"], self.collision_layer["world"],
                               self.collision_layer["enemy"]]) for pos in
                        enemy_positions]
        self.scene = EndScreen()
        # self.dashMeter = DashMeter(self.player.dashCooldown)
        self.healthBar = HealthBar()
        self.potionUI = PotionUI()
        self.level = level
        self.scene.level = self.level

        self.Transition = Transition()
        self.fade = self.Transition.fade
        self.fadeT = fade()
        self.next_level = 0

        self.hints = [(Object((270, 640)), "Hello")]
        self.dialogue = DialogueUI()

        self.paused = False
        self.PauseMenu = PauseMenu(self.level)

        self.seen_text = [False for _ in range(100)]  # Trust hardcoding at its best

        if self.level in [1, 3, 4]:
            # Density = total clouds / area
            # Total_clouds = area * density
            for i in range(round(MAP_WIDTH * SCREEN_HEIGHT * 2 / 3 * self.cloud_density)):
                Cloud((random.random() * MAP_WIDTH, random.random() * SCREEN_HEIGHT * 2 / 3), random.randint(100, 125))
        else:
            for particle in Setup.particles:
                if isinstance(particle, Cloud):
                    del Setup.particles[Setup.particles.index(particle)]
        self.sky = pg.image.load("Assets/world/sky_level_background.png").convert()

        try:
            if self.level == 1:
                pg.mixer.music.load("Assets/Music/Overworld_Music.ogg")
            if self.level == 2:
                pg.mixer.music.load("Assets/Music/Cave_Music.ogg")
                self.sky = pg.image.load("Assets/world/VOID.png").convert()

            if self.level == 3 or self.level == 4:
                pg.mixer.music.load("Assets/Music/Sky_Music.ogg")
            if self.level == 5:
                pg.mixer.music.load("Assets/Music/Combat_Music.ogg")
                self.sky = pg.image.load("Assets/world/VOID.png").convert()

            else:
                pg.mixer.music.load("Assets/Music/Overworld_Music.ogg")

            pg.mixer.music.play(-1)
        except:
            pass;

    # def load_world(self, level):

    def update(self, delta):
        if self.paused == True:
            self.level = self.PauseMenu.level
            pass
        else:
            Setup.camera_offset = self.player.update(delta)
            Setup.camera_offset.x = max(0, min(Setup.camera_offset.x, MAP_WIDTH - SCREEN_WIDTH))
            Setup.camera_offset.y = max(0, min(Setup.camera_offset.y, MAP_HEIGHT - SCREEN_HEIGHT))
            if self.player.dead:
                self.level = self.scene.level

            for i, enemy in enumerate(self.enemies):
                enemy.update(delta, self.player)
                if enemy.dead:
                    self.enemies[i] = PhysicsBody(enemy.position, enemy.velocity, enemy.width, enemy.height,
                                                  enemy.colour,
                                                  self.collision_layer["body"],
                                                  [self.collision_layer["world"], self.collision_layer["body"]])
                    self.collision_layer["enemy"].remove(enemy)
                    self.collision_layer["body"].add(self.enemies[i])

            for particle in particles:
                particle.update(delta)

            for event in pg.event.get(pg.KEYUP):
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        self.paused = True

            self.world.update(delta)
            self.fade = self.Transition.fade

            if self.level in [2, 5]:
                for particle in Setup.particles:
                    if isinstance(particle, Cloud):
                        del Setup.particles[Setup.particles.index(particle)]

        # self.pet.update(delta, self.player, self.camera_pos)

    def draw(self, surf):
        # screen.fill((0, 191, 255))

        # screen.fill((0, 191, 255))
        # screen.fill((255,255,255))
        surf.blit(self.sky, (0, 0))

        if (self.player.position[1] > 10000):
            self.player.dead = True

        # if (self.level in self.levels[2]):
        #     self.sky = pg.image.load("Assets/world/sky_level_background.png").convert()

        for particle in particles:
            particle.draw(surf)
        self.world.draw(surf)

        for potion in self.collision_layer["potion"]:
            potion.draw(surf)
        for spike in self.collision_layer["spike"]:
            spike.draw(surf)

        try:
            self.Transition.draw(surf, self.player.position, self.portal_position)
        except:
            pass;

        if (self.level == 1):
            # self.dialogue.draw(surf, self.enemies[0], "enemy dialogue")
            self.dialogue.draw(surf, self.player, "Press A or D to move.", 400, 0, 900, 1800)
            self.dialogue.draw(surf, self.player, "Press W or SPACE to jump.", 400, 0, 1800, 1750)
            self.dialogue.draw(surf, self.player, "Left click to attack.", 400, 0, 2400, 1540)
            self.dialogue.draw(surf, self.player, "Press 1 to heal using potions", 400, 0, 2400, 1580)
            # print(self.player.position)
            if self.seen_text[0] or self.player.position.x > 3000:
                self.seen_text[0] = True
                self.dialogue.draw(surf, self.player, "These goons must be guarding something!", 10, 1)
                self.dialogue.draw(surf, self.player, "It may just be what I am looking for...", 7, 2)
            if self.seen_text[1] or (self.player.position.y > 2500 and self.player.position.x > 6000):
                self.seen_text[0] = False
                self.seen_text[1] = True
                self.dialogue.draw(surf, self.player, "This treasure is pennies compared to what I'm after...", 10, 3)
                self.dialogue.draw(surf, self.player, "But this portal will bring me one dimension closer!", 10, 4)

        for enemy in self.enemies:
            enemy.draw(surf)

        self.player.draw(surf)

        # self.dialogue.draw(surf, self.player, "Next dimension, next portal...", 4, 1)
        # self.dialogue.draw(surf, self.player, "It's really that simple.", 4, 2)
        # for o,text in self.hints:
        #     o.position -= Setup.camera_offset
        #     self.dialogue.draw(surf,o, text)
        #     # a,b = createText(o.position.x,o.position.y,10,(0,0,0),"Regular",text)
        #
        #     # surf.blit(a,pg.Vector2(b)-Setup.camera_offset)
        #     # print(o.position,text,b)
        #     pg.draw.circle(surf,(255,0,0),o.position,10)
        #     o.position += Setup.camera_offset
        # self.dialogue.draw(surf, self.player, "text2", 3, 2)
        # self.dialogue.draw(surf, self.player, "text3", 2, 3)
        # self.dialogue.draw(surf, self.player, "text4", 1, 4)
        # self.dialogue.draw(surf, self.player, "text5", 0.5, 5)

        # self.dashMeter.update(self.player.lastDash)
        # self.dashMeter.draw(surf)
        self.healthBar.draw(surf, self.player.health)
        self.potionUI.draw(surf, self.player.potion_bag, self.player.potion_cooldown)

        # print(self.player.get_collision_rect())s
        # Debug Lines. DO NOT CROSS THEM!
        # pg.draw.line(surf, (255, 0, 0), -Setup.camera_offset, pg.Vector2(SCREEN_WIDTH, -Setup.camera_offset.y), 10)
        # pg.draw.line(surf, (255, 0, 0), -Setup.camera_offset, pg.Vector2(-Setup.camera_offset.x, SCREEN_HEIGHT), 10)
        # self.pet.draw(surf)

        if (self.fade == True):
            self.fadeT.update(True)
            self.fadeT.draw()
        else:
            self.fadeT.update()
            self.fadeT.draw()

        if (self.fadeT.transparency >= 255):
            self.Transition.fade = False
            self.next_level = self.level + 1
            self.level = -4

        if self.paused == True:
            self.PauseMenu.update(self)
            self.PauseMenu.draw()

        if self.player.dead:
            self.scene.update()
            self.scene.draw()
