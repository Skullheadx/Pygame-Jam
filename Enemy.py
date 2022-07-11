from argparse import Action
from Setup import *
from Player import Player
from Actors import Actor
from Weapon import Melee


class Enemy(Actor):
    speed = Actor.speed * 0.33
    jump_strength = Actor.jump_strength * 0.5
    colour = (235, 64, 52)
    friction = 0.9
    run_gif = Image.open("Assets/skeleton/skeleton_run.gif")
    run_frames = []
    for i in range(run_gif.n_frames):
        run_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(run_gif, i)), (125, 125)))
    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)

        self.areas = {
            "head": Area(self.position, pg.Vector2(self.width * 1 / 3 * 1 / 2, -2), self.width * 2 / 3, 25, Player,
                         self.knockout)}
        self.movable = False

        self.direction = -1

        # self.health = 0 # for debugging without getting killed

        self.weapon = Melee(self.position, (-Melee.width / 2 + 7, Melee.height / 2 + self.height / 3 - 8),
                            (-5, Melee.height), self.width, -1, -10)

        self.buffer = []

        self.display_offsets = {"enemy":pg.Vector2(0,0)}

        self.current_frame = 0
        self.display = self.run_frames[math.floor(self.current_frame)]
        self.state = "RUN"
        
    def update(self, delta, target=None):
        super().update(delta)
        if not self.attacked and target is not None and self.stun_time == 0:
            # print('a')
            self.follow_target(target)
            # if random.random() < 2/fps and not self.weapon.attacking and self.weapon.get_collision_rect().colliderect(target.get_collision_rect()):
            #     target.attack(self, self.weapon, self.direction)
            #     print('attack')

        # Deals with collision and applying velocity
        self.position, self.velocity = self.move_and_collide(self.position.copy(), self.velocity.copy(), delta)

        if self.velocity.x == 0:
            self.direction = 0
        else:
            self.direction = math.copysign(1, self.velocity.x)
        self.weapon.update(delta, self.position, self.direction)
        
        if self.state == "RUN":
            frame = math.floor(self.current_frame)
            if self.velocity.x > 0:
                self.display = self.run_frames[math.floor(frame)]
                self.display_offsets["enemy"] = pg.Vector2(-40, -35)
            elif self.velocity.x <= 0:
                self.display = pg.transform.flip(self.run_frames[math.floor(frame)], True, False)
                self.display_offsets["enemy"] = pg.Vector2(-55, -35)

            self.current_frame = (self.current_frame + 0.5) % self.run_gif.n_frames
            

        # print(self.velocity)

    def knockout(self, node):
        self.stun_time = 100
        self.modify_health(-25, None)
        node.on_ground = False
        node.push(math.copysign(1, node.velocity.x), 0.25, -2.25)
        # self.crouch(1000)

    def draw(self, surf):
        self.weapon.draw(surf)
        # super(Enemy, self).draw(surf)
        surf.blit(self.display, get_display_rect(self.get_collision_rect()).topleft + self.display_offsets["enemy"])

        # for b in self.buffer:
        #     pg.draw.rect(surf,(0,0,255),get_display_rect(b),3)
        # self.buffer.append(self.get_collision_rect())
        # pg.draw.rect(surf, (0, 255, 0), get_display_rect(self.get_collision_rect()), 2)
