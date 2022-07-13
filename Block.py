from Setup import *


class Block:
    textures = {file[:file.index(".")]:pg.transform.scale(
        pg.image.load(path.join("Assets/world/blocks", file)), (50, 50)) for
                   file in listdir("Assets/world/blocks")}
    textures = {name: surf.convert() for name, surf in textures.items()}

    width, height = textures["PLACEHOLDER"].get_size()
    colour = (71, 77, 97)

    def __init__(self, pos, collision_layer, texture="PLACEHOLDER"):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0,0) # So that we may have moving blocks
        collision_layer.add(self)

        self.texture = self.textures[texture]

        self.movable = False

    def update(self, delta):
        pass

    def get_collision_rect(self):
        return pg.Rect(self.position, (self.width, self.height))

    def draw(self, surf):
        # pg.draw.rect(surf, self.colour, get_display_rect(self.get_collision_rect()), border_radius=3)
        display_rect = get_display_rect(self.get_collision_rect())
        if display_rect.colliderect(screen_rect):
            surf.blit(self.texture, display_rect)
