import Setup
from Setup import *

class Dust:
    dust_gif = Image.open("Assets/player/DUSTCLOUD.gif")
    dust_frames = []
    for i in range(dust_gif.n_frames):
        dust_frames.append(pil_to_game(get_gif_frame(dust_gif, i)))

    def __init__(self, pos, dust_size, direction):
        self.position = pg.Vector2(pos)
        self.dust_size = dust_size
        self.velocity = pg.Vector2(0,0)
        self.direction = -direction
        self.current_frame = 0
        self.display = self.dust_frames[math.floor(self.current_frame)]
        Setup.particles.append(self)

    def update(self, delta):
        self.position += self.velocity
        self.velocity = pg.Vector2(self.direction * delta / 64, -self.current_frame * delta / 256)
        self.display = pg.transform.scale(self.dust_frames[math.floor(self.current_frame)], (self.dust_size, self.dust_size))
        self.current_frame = (self.current_frame + 0.25)
        if math.floor(self.current_frame) >= self.dust_gif.n_frames-1:
            del Setup.particles[Setup.particles.index(self)]

    def draw(self, surf):
        surf.blit(self.display, get_display_point(self.position))

class Cloud:
    img = pg.image.load("Assets/world/CLOUD.png")

    def __init__(self, pos, cloud_size):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(random.random()/5000,0)
        self.cloud_size = cloud_size
        self.display_img = pg.transform.scale(self.img, (self.cloud_size, self.cloud_size))
        Setup.particles.append(self)

    def update(self, delta):
        self.position += self.velocity * delta

    def draw(self, surf):
        surf.blit(self.display_img, self.position - Setup.camera_offset * 0.25)
