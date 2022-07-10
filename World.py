from Setup import *
from Block import Block
from os import path


class World:

    def __init__(self, collision_layer):
        self.collision_layer = collision_layer
        self.blocks = []

    def load_world(self, level):
        with open(path.join("Levels", f'Level{level}.txt'), 'r') as f:
            file_contents = f.read().split("\n")

        out = [[], center]
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
                else:
                    self.blocks.append(Block((x, y), self.collision_layer[l], t))
        return out

    def update(self, delta):
        for block in self.blocks:
            block.update(delta)

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)
