from Setup import *
from Actors import Actor
from Player import Player

class Pet(Actor):
    width,height = 35,25
    speed = Player.speed * 0.75
    jump_strength = Player.jump_strength / 2

    move_gif = Image.open("Assets/SNAKE.gif")
    move_frames = []
    #for i in range(move_gif.n_frames):
        #idk how this works
        #move_frames.append(pg.transform.scale(pil_to_game(get_gif_frame(move_gif, i)), (200, 200)))

    def __init__(self, pos, collision_layer, collision_mask):
        super().__init__(pos, collision_layer, collision_mask)
    
    def update(self, delta, target):
        super().update(delta)

        self.follow_target(target, stop_dist=70)

        self.position, self.velocity = self.move_and_collide(self.position, self.velocity, delta)
