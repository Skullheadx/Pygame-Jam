import random

import Setup
from EndScreen import EndScreen
from Enemy import Enemy, Skeleton, King
from Function.Fade import fade
from Function.Portal import Transition
from Item import PotionItem
from Object import Object
from Particle import Cloud, Treasure
from PauseMenu import PauseMenu
from Pet import Pet
from PhysicsBody import PhysicsBody
from Player import Player
from Setup import *
from Spike import Spike
from UI.Dialogue import DialogueUI
from UI.HealthBar import BossHealthBar, HealthBar
from UI.PotionUI import PotionUI
from World import World
from RangedAttack import RangedAttack


class Game:
    cloud_density = 1 / 1000
    saved_jeff = False

    def __init__(self, level):
        self.collision_layer = {"none": set(), "world": set(), "player": set(), "enemy": set(), "pet": set(),
                                "body": set(), "potion": set(), "spike": set(), "arrow": set()}

        # self.load_world(level)

        self.levels = [[], [], [3, 4]]

        self.world = World(self.collision_layer)

        enemy_positions, player_position, self.portal_position, heal_positions, spike_positions, self.skele_positions, king_position, jeff_position = self.world.load_world(
            level)

        for i in heal_positions:
            PotionItem(i, self.collision_layer["potion"])
        for i in spike_positions:
            Spike(i, self.collision_layer["spike"])
        if king_position is not None:
            self.king = King(king_position, self.collision_layer["enemy"],
                             [self.collision_layer["player"], self.collision_layer["world"],
                              self.collision_layer["enemy"]],
                             (self.collision_layer["world"], self.collision_layer["arrow"]))
            self.treasure = [Treasure(self.king.position - pg.Vector2(0, 50),pg.Vector2((random.random() -0.5) * 2, random.random() -2.5), self.collision_layer["body"],
                                      [self.collision_layer["world"]]) for i in range(10)]
        else:
            self.king = None
            self.treasure = None

        self.player = Player(player_position, self.collision_layer["player"],
                             [self.collision_layer["enemy"], self.collision_layer["world"]],
                             [self.collision_layer["enemy"], self.collision_layer["body"]],
                             self.collision_layer["potion"],
                             self.collision_layer["spike"],
                             self.collision_layer["arrow"])
        if(level == 1):
            self.pet = Pet([6852, 1500], self.collision_layer["pet"], [self.collision_layer["world"]])
        else:
            self.pet = Pet(self.player.position - [100000, 100000], self.collision_layer["pet"], [self.collision_layer["world"]])
        self.has_pet = False
        if jeff_position is not None:
            self.jeff = Enemy(jeff_position, self.collision_layer["enemy"],
                              [self.collision_layer["player"], self.collision_layer["world"],
                               self.collision_layer["enemy"]],is_jeff=True)
            self.jeff_target = [self.player]
        else:
            self.jeff = None
        # self.pet = Pet(center, self.collision_layer["pet"], [self.collision_layer["world"]])
        self.enemies = [Enemy(pos, self.collision_layer["enemy"],
                              [self.collision_layer["player"], self.collision_layer["world"],
                               self.collision_layer["enemy"]]) for pos in
                        enemy_positions]
        self.skeletons = [Skeleton(pos, self.collision_layer["enemy"],
                                   [self.collision_layer["player"], self.collision_layer["world"],
                                    self.collision_layer["enemy"]]) for pos in
                          self.skele_positions]
        self.allies = [Enemy(self.player.position + pg.Vector2(-150,-200), self.collision_layer["pet"],
                              [self.collision_layer["pet"], self.collision_layer["world"],
                               self.collision_layer["enemy"]]) for i in
                        range(1)]
        for ally in self.allies:
            ally.stun_time = 10000
            ally.weapon.damage = -10



        self.scene = EndScreen()
        # self.dashMeter = DashMeter(self.player.dashCooldown)
        self.healthBar = HealthBar()
        self.potionUI = PotionUI()
        self.bosshealthBar = BossHealthBar()
        self.level = level
        self.scene.level = self.level
        if self.level == 4 and self.saved_jeff:
            self.jeff_target = self.skeletons
            self.jeff = Enemy(self.player.position + pg.Vector2(-50, -500), self.collision_layer["pet"],
                              [self.collision_layer["pet"], self.collision_layer["world"],
                               self.collision_layer["enemy"]],is_jeff=True)
            self.jeff.stun_time = 10000
            self.jeff.weapon.damage = -10

        self.Transition = Transition()
        self.fade = self.Transition.fade
        self.fadeT = fade()
        self.next_level = 0

        # self.hints = [(Object((270, 640)), "Hello")]
        self.dialogue = DialogueUI()

        self.skeleton_spawn_frame = pg.transform.scale(
            pil_to_game(get_gif_frame(Image.open("Assets/skeleton/skeleton_attack.gif"), 0)), (170, 138))
        self.skeleton_spawn_coords = []
        skeleton_portal_gif = Image.open("Assets/skeleton/portal.gif")
        self.skeleton_portal_gif = []
        for i in range(skeleton_portal_gif.n_frames):
            self.skeleton_portal_gif.append(
                pg.transform.scale(pil_to_game(get_gif_frame(skeleton_portal_gif, i)), (96, 64)))

        self.paused = False
        self.PauseMenu = PauseMenu(self.level)

        self.seen_text = [False for _ in range(100)]  # Trust hardcoding at its best

        if self.level in [1, 3]:
            # Density = total clouds / area
            # Total_clouds = area * density
            if self.level == 3:
                for i in range(round(SCREEN_WIDTH * SCREEN_HEIGHT * self.cloud_density)):
                    Cloud((random.random() * MAP_WIDTH, get_display_point(self.player.position).y - 1700 + random.random() * SCREEN_HEIGHT), random.randint(100, 125))
            elif self.level == 1:
                for i in range(round(SCREEN_WIDTH * SCREEN_HEIGHT * self.cloud_density)):
                    Cloud((random.random() * MAP_WIDTH, random.random() * SCREEN_HEIGHT * 2/3 + 50), random.randint(100, 125))
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
            pg.mixer.music.set_volume(0.5)

        except:
            pass;
        # self.test = RangedAttack((1650,1250),self.collision_layer["world"], self.collision_layer["arrow"])
        if(self.level == 4):
            self.portal_position = (5475, 2400)
    # def load_world(self, level):

    def update(self, delta):
        # self.test.update(delta)
        if self.paused == True:
            self.level = self.PauseMenu.level
            pass
        elif self.player.dead:
            self.level = self.scene.level
            pg.mixer.stop()
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
                    if enemy in self.collision_layer["enemy"]:
                        self.collision_layer["enemy"].remove(enemy)
                    self.collision_layer["body"].add(self.enemies[i])
            if self.saved_jeff:
                for i, enemy in enumerate(self.allies):
                    min_distance = 100000000
                    target = None
                    for skele in self.skeletons:
                        if isinstance(skele, PhysicsBody):
                            continue
                        if min_distance > (skele.position - enemy.position).length_squared():
                            min_distance = (skele.position - enemy.position).length_squared()
                            target = skele
                    if self.king is not None and (self.king.position - enemy.position).length_squared() < min_distance:
                        target = self.king
                    enemy.update(delta, target, 10000000)
            for i, enemy in enumerate(self.skeletons):
                enemy.update(delta, self.player)
                if enemy.dead:
                    self.skeletons[i] = PhysicsBody(enemy.position, enemy.velocity, enemy.width, enemy.height / 2,
                                                    enemy.colour,
                                                    self.collision_layer["body"],
                                                    [self.collision_layer["world"], self.collision_layer["body"]],
                                                    goon_skin=False)
                    if enemy in self.collision_layer["enemy"]:
                        self.collision_layer["enemy"].remove(enemy)
                    self.collision_layer["body"].add(self.skeletons[i])
            if self.king is not None:
                self.king.update(delta, self.player)
                if isinstance(self.king, PhysicsBody):
                    for t in self.treasure:
                        t.update(delta, self.king.position)
                if self.king.dead:
                    self.collision_layer["enemy"].remove(self.king)
                    self.king = PhysicsBody(self.king.position, self.king.velocity, self.king.width / 2,
                                            self.king.height / 4,
                                            self.king.colour,
                                            self.collision_layer["body"],
                                            [self.collision_layer["world"], self.collision_layer["body"]],
                                            goon_skin=False)
                    self.collision_layer["body"].add(self.king)
                    for i, enemy in enumerate(self.skeletons):
                        if enemy in self.collision_layer["enemy"]:
                            self.collision_layer["enemy"].remove(enemy)
                        self.skeletons[i] = PhysicsBody(enemy.position, enemy.velocity, enemy.width, enemy.height,
                                                        enemy.colour,
                                                        self.collision_layer["body"],
                                                        [self.collision_layer["world"], self.collision_layer["body"]],
                                                        goon_skin=False)
                        self.collision_layer["body"].add(self.skeletons[i])
            if self.jeff is not None:
                # if isinstance(self.jeff_target[0], Skeleton):

                if self.jeff_target[0] == self.player:
                    self.jeff.update(delta, self.player)
                    if self.jeff.dead:
                        self.collision_layer["enemy"].remove(self.jeff)
                        self.jeff = PhysicsBody(self.jeff.position, self.jeff.velocity, self.jeff.width,
                                                self.jeff.height,
                                                self.jeff.colour,
                                                self.collision_layer["body"],
                                                [self.collision_layer["world"], self.collision_layer["body"]],
                                                goon_skin=False, is_jeff=True)
                        self.collision_layer["body"].add(self.jeff)
                else:
                    min_distance = 100000000
                    target = None
                    for skele in self.skeletons:
                        if isinstance(skele, PhysicsBody):
                            continue
                        if min_distance > (skele.position - self.jeff.position).length_squared():
                            min_distance = (skele.position - self.jeff.position).length_squared()
                            target = skele
                    if (self.king.position - self.jeff.position).length_squared() < min_distance:
                        target = self.king
                    self.jeff.update(delta, target, 10000000)

            for particle in particles:
                particle.update(delta)

            for event in pg.event.get(pg.KEYUP):
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        self.paused = True

            self.world.update(delta)
            self.fade = self.Transition.fade

            if self.level == 3 and self.fade:
                if self.jeff.position.y < 10000 and (isinstance(self.jeff, PhysicsBody) and not self.jeff.was_beaten):
                    self.saved_jeff = True
                else:
                    self.saved_jeff = False

            if self.level in [2, 5]:
                for particle in Setup.particles:
                    if isinstance(particle, Cloud):
                        del Setup.particles[Setup.particles.index(particle)]

            if self.level == 4:
                self.bosshealthBar.update()

            if self.level == 1:
                # print(self.player.position)
                if self.player.position[0] > 6750 and self.player.position[1] >= 1500:
                    self.has_pet = True
                self.pet.has_pet = self.has_pet

            if self.has_pet == True:
                self.pet.update(delta, self.player)
                #update pet

        # self.pet.update(delta, self.player, self.camera_pos)

    def draw(self, surf):

        # screen.fill((0, 191, 255))

        # screen.fill((0, 191, 255))
        # screen.fill((255,255,255))
        surf.blit(self.sky, (0, 0))

        if (self.level == 4):
            # print(get_camera_offset())
            if self.king is not None and isinstance(self.king, King):
                if self.king.skeleton_attack == True:
                    for i in range(random.randint(1, 2)):
                        if(len(self.skeleton_spawn_coords) < 2):
                            self.skeleton_spawn_coords.append([(random.randint(4000, 5000), random.randint(3250, 3350)), 0])
                    self.king.skeleton_attack = False


            for i in range(len(self.skeleton_spawn_coords)):
                try:
                    surf.blit(self.skeleton_portal_gif[self.skeleton_spawn_coords[i][1]],
                              get_display_point((self.skeleton_spawn_coords[i][0][0] + 40, 3150)))

                    if (self.skeleton_spawn_coords[i][0][1] <= 3050):
                        skele = Skeleton(self.skeleton_spawn_coords[i][0], self.collision_layer["enemy"],
                                         [self.collision_layer["player"], self.collision_layer["world"],
                                          self.collision_layer["enemy"]])
                        self.skeletons.append(skele)
                        self.skeleton_spawn_coords[i][0] = (100000, 100000)
                    else:
                        lst = list(self.skeleton_spawn_coords[i][0])
                        lst[1] -= 2
                        self.skeleton_spawn_coords[i][0] = tuple(lst)
                        surf.blit(self.skeleton_spawn_frame, get_display_point(self.skeleton_spawn_coords[i][0]))
                        if (self.skeleton_spawn_coords[i][1] <= 5):
                            self.skeleton_spawn_coords[i][1] += 1

                    if (self.skeleton_spawn_coords[i][0][0] > 50000 and self.skeleton_spawn_coords[i][0][1] > 50000):
                        self.skeleton_spawn_coords[i][1] -= 1
                        if (self.skeleton_spawn_coords[i][1] >= 0):
                            self.skeleton_spawn_coords.pop(i)
                except IndexError:
                    pass;

        if self.king is not None and isinstance(self.king, PhysicsBody):
            self.Transition.update()
            self.Transition.draw(surf, self.player.position, self.portal_position)
            if(self.portal_position[1] < 3150):
                lst = list(self.portal_position)
                lst[1] += 10
                self.portal_position = tuple(lst)
                # print(get_camera_offset(), getWorldCoords(0, 0))
        
        if (self.player.position[1] > 10000):
            self.player.dead = True

        # if (self.level in self.levels[2]):
        #     self.sky = pg.image.load("Assets/world/sky_level_background.png").convert()

        for particle in particles:
            particle.draw(surf)
        self.world.draw(surf)

        if isinstance(self.king, PhysicsBody):
            for t in self.treasure:
                t.draw(surf)

        for potion in self.collision_layer["potion"]:
            potion.draw(surf)
        for spike in self.collision_layer["spike"]:
            spike.draw(surf)

        try:
            self.Transition.draw(surf, self.player.position, self.portal_position)
        except:
            pass;

        self.pet.draw(surf, self.player.position)

        if (self.level == 1):
            # self.dialogue.draw(surf, self.enemies[0], "enemy dialogue")
            self.dialogue.draw(surf, self.player, "Press A or D to move.", 400, 0, 900, 1800)
            self.dialogue.draw(surf, self.player, "Press W or SPACE to jump.", 400, 0, 1800, 1750)
            self.dialogue.draw(surf, self.player, "Left click to attack.", 400, 0, 2400, 1540)
            self.dialogue.draw(surf, self.player, "Press 1 to heal using potions", 400, 0, 2400, 1580)
            self.dialogue.draw(surf, self.player, "This way ->", 400, 0, 5600, 1500)
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
        elif self.level == 2:
            if self.seen_text[0] or self.player.position.x > 16500:
                self.seen_text[0] = True
                self.dialogue.draw(surf, self.player, "More of them!?", 10, 1)
                self.dialogue.draw(surf, self.player, "They must be looking for the Realm of Secrets too...", 10, 2)
            if self.seen_text[1] or (self.player.position.y > 8500 and self.player.position.x > 18000):
                self.seen_text[0] = False
                self.seen_text[1] = True
                self.dialogue.draw(surf, self.player, "Shoot! They got to the portal already!", 10, 3)
                self.dialogue.draw(surf, self.player, "I can't let those goons get another second ahead of me.", 10, 4)
        elif self.level == 3:
            if self.seen_text[0] or self.player.position.x > 13000:
                self.seen_text[0] = True
                self.dialogue.draw(surf, self.player, "I suppose you are the captain...", 5, 1)
                self.dialogue.draw(surf, self.jeff, "That's me. And the treasure is MINE!", 7,2)
            if self.seen_text[1] or isinstance(self.jeff, PhysicsBody):
                # self.seen_text[5] = False
                self.seen_text[1] = True
                self.dialogue.draw(surf, self.jeff, "Noooo! Please don't kill me!", 5, 3)
                self.dialogue.draw(surf, self.player, "...", 5, 4)
        elif self.level == 4:
            # print(self.player.position)
            if self.seen_text[0] or True:
                self.seen_text[0] = True
                if self.jeff is not None:
                    self.dialogue.draw(surf, self.jeff, "You didn't kill us... So we'll help you.", 5, 0, 1890, 3350)
                self.dialogue.draw(surf, self.player, "Here it is... The greatest treasure of all time and space...", 5, 1)
            if self.seen_text[1] or self.player.position.x > 5000:
                self.seen_text[1] = True
                self.dialogue.draw(surf, self.king, "I am the Bone King! The protector of this dimension and NONE shall pass!", 20,2)
            if self.seen_text[2] or isinstance(self.king, PhysicsBody):
                self.seen_text[2] = True
                if self.jeff is not None:
                    self.dialogue.draw(surf, self.jeff, "We have won! Go through the portal... the honour is yours", 20,2)



        if self.saved_jeff:
            for enemy in self.allies:
                enemy.draw(surf)
        for enemy in self.enemies:
            enemy.draw(surf)
        for enemy in self.skeletons:
            enemy.draw(surf)

        if self.king is not None:
            self.king.draw(surf)
        if self.jeff is not None:
            self.jeff.draw(surf)
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
        if self.level == 4:
            self.bosshealthBar.draw(surf, self.king.health)
        # print(self.player.get_collision_rect())s
        # Debug Lines. DO NOT CROSS THEM!
        # pg.draw.line(surf, (255, 0, 0), -Setup.camera_offset, pg.Vector2(SCREEN_WIDTH, -Setup.camera_offset.y), 10)
        # pg.draw.line(surf, (255, 0, 0), -Setup.camera_offset, pg.Vector2(-Setup.camera_offset.x, SCREEN_HEIGHT), 10)

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

        # print(get_display_point(self.player.position))
        # print(self.player.position)

        # if self.player.has_pet == True:
        #     self.pet.draw(surf, self.player.position)
        #     pass
            #draw pet
