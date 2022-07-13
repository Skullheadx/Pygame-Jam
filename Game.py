import Setup
from EndScreen import EndScreen
from Enemy import Enemy, Skeleton, King
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
from RangedAttack import RangedAttack

class Game:
    cloud_density = 1 / 100000

    def __init__(self, level):
        self.collision_layer = {"none": set(), "world": set(), "player": set(), "enemy": set(), "pet": set(),
                                "body": set(), "potion": set(), "spike": set(), "arrow":set()}


        # self.load_world(level)

        self.levels = [[], [], [3, 4]]

        self.world = World(self.collision_layer)

        enemy_positions, player_position, self.portal_position, heal_positions, spike_positions, self.skele_positions, king_position = self.world.load_world(
            level)

        for i in heal_positions:
            PotionItem(i, self.collision_layer["potion"])
        for i in spike_positions:
            Spike(i, self.collision_layer["spike"])

        self.player = Player(player_position, self.collision_layer["player"],
                             [self.collision_layer["enemy"], self.collision_layer["world"]],
                             [self.collision_layer["enemy"], self.collision_layer["body"]],
                             self.collision_layer["potion"],
                             self.collision_layer["spike"],
                             self.collision_layer["arrow"])
        # self.pet = Pet(center, self.collision_layer["pet"], [self.collision_layer["world"]])
        self.enemies = [Enemy(pos, self.collision_layer["enemy"],
                              [self.collision_layer["player"], self.collision_layer["world"],
                               self.collision_layer["enemy"]]) for pos in
                        enemy_positions]
        self.skeletons = [Skeleton(pos, self.collision_layer["enemy"],
                                   [self.collision_layer["player"], self.collision_layer["world"],
                                    self.collision_layer["enemy"]]) for pos in
                          self.skele_positions]
        if king_position is not None:
            self.king = King(king_position, self.collision_layer["enemy"],
                             [self.collision_layer["player"], self.collision_layer["world"],
                              self.collision_layer["enemy"]],(self.collision_layer["world"], self.collision_layer["arrow"]))
        else:
            self.king = None

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

        # self.hints = [(Object((270, 640)), "Hello")]
        self.dialogue = DialogueUI()
        
        self.skeleton_spawn_frame = pg.transform.scale(pil_to_game(get_gif_frame(Image.open("Assets/skeleton/skeleton_attack.gif"), 0)), (170, 138))
        self.skeleton_spawn_coords = []
        skeleton_portal_gif = Image.open("Assets/skeleton/portal.gif")
        self.skeleton_portal_gif = []
        for i in range(skeleton_portal_gif.n_frames):
            self.skeleton_portal_gif.append(pg.transform.scale(pil_to_game(get_gif_frame(skeleton_portal_gif, i)), (96, 64)))
        
        

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

            if self.level == 3:
                pg.mixer.music.load("Assets/Music/Sky_Music.ogg")
            if self.level == 4:
                pg.mixer.music.load("Assets/Music/Combat_Music.ogg")
                self.sky = pg.image.load("Assets/world/VOID.png").convert()

            else:
                pg.mixer.music.load("Assets/Music/Overworld_Music.ogg")


            pg.mixer.music.play(-1)
        except:
            pass;
        # self.test = RangedAttack((1650,1250),self.collision_layer["world"], self.collision_layer["arrow"])

    # def load_world(self, level):

    def update(self, delta):
        # self.test.update(delta)
        if self.paused == True:
            self.level = self.PauseMenu.level
            pass
        elif self.player.dead:
            self.level = self.scene.level
            pass;
        else:
            Setup.camera_offset = self.player.update(delta)
            Setup.camera_offset.x = max(0, min(Setup.camera_offset.x, MAP_WIDTH - SCREEN_WIDTH))
            Setup.camera_offset.y = max(0, min(Setup.camera_offset.y, MAP_HEIGHT - SCREEN_HEIGHT))
            
            for i, enemy in enumerate(self.enemies):
                enemy.update(delta, self.player)
                if enemy.dead:
                    self.enemies[i] = PhysicsBody(enemy.position, enemy.velocity, enemy.width, enemy.height,
                                                  enemy.colour,
                                                  self.collision_layer["body"],
                                                  [self.collision_layer["world"], self.collision_layer["body"]])
                    self.collision_layer["enemy"].remove(enemy)
                    self.collision_layer["body"].add(self.enemies[i])
            for i, enemy in enumerate(self.skeletons):
                enemy.update(delta, self.player)
                if enemy.dead:
                    self.skeletons[i] = PhysicsBody(enemy.position, enemy.velocity, enemy.width, enemy.height,
                                                  enemy.colour,
                                                  self.collision_layer["body"],
                                                  [self.collision_layer["world"], self.collision_layer["body"]], goon_skin=False)
                    self.collision_layer["enemy"].remove(enemy)
                    self.collision_layer["body"].add(self.skeletons[i])
            if self.king is not None:
                self.king.update(delta, self.player)
                if self.king.dead:
                    print("You win!")

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

        if (self.level == 5 or self.level == 7):
            if self.king is not None:
                if self.king.skeleton_attack == True:
                    for i in range(random.randint(1, 2)):
                        if(len(self.collision_layer["enemy"]) < 4 and len(self.skeleton_spawn_coords) < 2):
                            self.skeleton_spawn_coords.append([(random.randint(1100, 2000), random.randint(1900, 2100)), 0])
                    self.king.skeleton_attack = False

            for i in range(len(self.skeleton_spawn_coords)):
                try:
                    surf.blit(self.skeleton_portal_gif[self.skeleton_spawn_coords[i][1]], get_display_point((self.skeleton_spawn_coords[i][0][0] + 40, 1849)))  

                    if(self.skeleton_spawn_coords[i][0][1] <= 1780):
                        skele = Skeleton(self.skeleton_spawn_coords[i][0], self.collision_layer["enemy"], [self.collision_layer["player"],self.collision_layer["world"],self.collision_layer["enemy"]])
                        self.skeletons.append(skele)
                        self.skeleton_spawn_coords[i][0] = (100000, 100000)
                    else:
                        lst = list(self.skeleton_spawn_coords[i][0])
                        lst[1] -= 2
                        self.skeleton_spawn_coords[i][0] = tuple(lst)
                        surf.blit(self.skeleton_spawn_frame, get_display_point(self.skeleton_spawn_coords[i][0]))
                        if(self.skeleton_spawn_coords[i][1] <= 5):
                            self.skeleton_spawn_coords[i][1] += 1
                    
                    if(self.skeleton_spawn_coords[i][0][0] > 50000 and self.skeleton_spawn_coords[i][0][1] > 50000):
                        self.skeleton_spawn_coords[i][1] -= 1
                        if(self.skeleton_spawn_coords[i][1] >= 0):
                            self.skeleton_spawn_coords.pop(i)
                except IndexError:
                    pass;
        
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
                self.dialogue.draw(surf, self.player, "It may just be what I am looking for...", 10, 2)
            if self.seen_text[1] or (self.player.position.y > 2500 and self.player.position.x > 6000):
                self.seen_text[0] = False
                self.seen_text[1] = True
                self.dialogue.draw(surf, self.player, "This treasure is pennies compared to what I'm after...", 10, 3)
                self.dialogue.draw(surf, self.player, "But this portal will bring me one dimension closer!", 10, 4)

        for enemy in self.enemies:
            enemy.draw(surf)
        for enemy in self.skeletons:
            enemy.draw(surf)

        if self.king is not None:
            self.king.draw(surf)
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

        if (self.fadeT.transparency >= 255 and self.player.dead == False):
            self.Transition.fade = False
            self.next_level = self.level + 1
            self.level = -4

        if self.paused == True:
            self.PauseMenu.update(self)
            self.PauseMenu.draw()

        if self.player.dead:
            self.scene.update()
            self.scene.draw()
