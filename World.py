from Setup import *
from Block import Block
from Item import PotionItem
from os import path, listdir


class World:

    def __init__(self, collision_layer):
        self.collision_layer = collision_layer
        self.blocks = []

    def load_world(self, level):
        with open(path.join("Levels", f'Level{level}.txt'), 'r') as f:
            file_contents = f.read().split("\n")

        out = [[], center, "a", []]
        for i in range(0, len(file_contents) - 1, 3):
            layer = file_contents[i].split("|")
            pos = file_contents[i + 1].split("|")
            texture = file_contents[i + 2].split("|")

            for l, p, t in zip(layer, pos, texture):
                if p == "":
                    break
                x, y = p.split(',')
                x = float(x)
                y = float(y)
                if t == "PLAYER":
                    out[1] = (x, y)
                elif t == "ENEMY":
                    out[0].append((x, y))
                elif t == "PORTAL":
                    out[2] = (x, y)
                elif t == "HEALTHPOTION":
                    out[3].append((x,y))
                elif f"{t}.png" in listdir("Assets/world/decor"):
                    self.blocks.append(Decor((x,y),self.collision_layer["none"],t))
                else:
                    self.blocks.append(Block((x, y), self.collision_layer[l], t))
        return out

    def update(self, delta):
        for block in self.blocks:
            block.update(delta)

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)


class Decor:
    textures = dict()
    # for file in listdir("Assets/world/decor"):
    #     textures[file[:file.index(".")]] = pg.transform.scale(
    #     pg.image.load(path.join("Assets/world/decor", file)), (50, 50))
    for file in listdir("Assets/world/decor"):
        img = pg.image.load(path.join("Assets/world/decor", file))

        textures[file[:file.index(".")]] = pg.transform.scale(pg.image.load(path.join("Assets/world/decor", file)),(img.get_width() * 50/16, img.get_height() * 50/16))
    def __init__(self, pos, collision_layer, img):
        self.position = pg.Vector2(pos)
        self.img = img
        collision_layer.add(self)

    def update(self, delta):
        pass

    def draw(self, surf):
        surf.blit(self.textures[self.img],get_display_point(self.position))
