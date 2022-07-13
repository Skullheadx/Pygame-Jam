from Setup import *
from Actors import Actor
from Player import Player

class Pet(Actor):
    width,height = 35,25
    speed = Player.speed * 0.75
    jump_strength = Player.jump_strength / 2

    move_gif = Image.open("Assets/SNAKE.gif")
    move_frames = []
    for i in range(move_gif.n_frames):
        move_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(move_gif, i)), (50, 50)))

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)
        self.frame = 0
    
    def update(self, delta, target):
        super().update(delta)

        self.follow_target(target, stop_dist=70)

        self.position, self.velocity = self.move_and_collide(self.position, self.velocity, delta)

    def draw(self, surf, plpos=0):

        d_off = pg.Vector2(0, -10)

        display = self.move_frames[math.floor(self.frame)]
        if(self.velocity[0] > 0):
            display = pg.transform.flip(display, True, False)

        surf.blit(display, get_display_rect(self.get_collision_rect()).topleft + d_off)
        diff = self.position - plpos
        if(abs(diff[0]) >= 1500 or abs(diff[1]) >= 1000):
            self.position = plpos

        if(self.frame + 0.1 < len(self.move_frames)):
            self.frame += 0.08
        else: self.frame = 0
