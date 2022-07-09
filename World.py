from Setup import *
from Block import Block
from os import path


class World:

    def __init__(self, collision_layer):
        self.collision_layer = collision_layer
        self.blocks = []
        self.level = 1
        self.add_world(self.level)

    def add_world(self, level):
        with open(path.join("Levels", f'Level{level}.txt'), 'r') as f:
            file_contents = f.read().split("\n")


        for i in range(0,len(file_contents)-1,3):
            layer = file_contents[i].split("|")
            pos = file_contents[i+1].split("|")
            texture = file_contents[i+2].split("|")

            for l,p,t in zip(layer,pos,texture):
                if p == "":
                    break
                x,y = p.split(',')
                self.blocks.append(Block((float(x),float(y)),self.collision_layer[l],t))

    def update(self, delta):
        for block in self.blocks:
            block.update(delta)

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)
