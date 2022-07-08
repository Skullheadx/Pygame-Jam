from Setup import *
from Block import Block

class World:

    def __init__(self, collision_layer):
        self.collision_layer = collision_layer
        self.blocks = []
        self.add_world()

    def add_world(self):
        for i in range(25):
            self.blocks.append(Block((i * Block.width,SCREEN_HEIGHT*3/4),self.collision_layer["world"],"GRASS"))
            self.blocks.append(Block((i * Block.width,SCREEN_HEIGHT*3/4 + Block.height),self.collision_layer["world"],"DIRT"))
            if random.random() < 0.5:
                self.blocks.append(
                    Block((i * Block.width, SCREEN_HEIGHT * 3 / 4 + Block.height * 2), self.collision_layer["world"],
                          "STONE"))
            else:
                self.blocks.append(
                    Block((i * Block.width, SCREEN_HEIGHT * 3 / 4 + Block.height * 2), self.collision_layer["world"],
                          "DIRT"))
            self.blocks.append(Block((i * Block.width,SCREEN_HEIGHT*3/4 + Block.height * 3),self.collision_layer["world"],"STONE"))
            self.blocks.append(Block((i * Block.width,SCREEN_HEIGHT*3/4 + Block.height * 4),self.collision_layer["world"],"STONE"))

        self.blocks.append(Block((Block.width * 10,SCREEN_HEIGHT*3/4 + Block.height * -1),self.collision_layer["none"],"TREEBARK"))
        self.blocks.append(Block((Block.width * 10,SCREEN_HEIGHT*3/4 + Block.height * -2),self.collision_layer["none"],"TREEBARK"))
        self.blocks.append(Block((Block.width * 10,SCREEN_HEIGHT*3/4 + Block.height * -3),self.collision_layer["none"],"TREEBARK"))
        self.blocks.append(Block((Block.width * 10,SCREEN_HEIGHT*3/4 + Block.height * -4),self.collision_layer["none"],"TREEBARK"))

        self.blocks.append(Block((Block.width * 10,SCREEN_HEIGHT*3/4 + Block.height * -3),self.collision_layer["none"],"LEAFS"))
        self.blocks.append(Block((Block.width * 10,SCREEN_HEIGHT*3/4 + Block.height * -4),self.collision_layer["none"],"LEAFS"))
        self.blocks.append(Block((Block.width * 10,SCREEN_HEIGHT*3/4 + Block.height * -5),self.collision_layer["none"],"LEAFS"))
        # self.blocks.append(Block((Block.width * 10,SCREEN_HEIGHT*3/4 + Block.height * -6),self.collision_layer["none"],"LEAFS"))

        self.blocks.append(Block((Block.width * 9,SCREEN_HEIGHT*3/4 + Block.height * -3),self.collision_layer["none"],"LEAFS"))
        self.blocks.append(Block((Block.width * 9,SCREEN_HEIGHT*3/4 + Block.height * -4),self.collision_layer["none"],"LEAFS"))
        self.blocks.append(Block((Block.width * 9,SCREEN_HEIGHT*3/4 + Block.height * -5),self.collision_layer["none"],"LEAFS"))
        # self.blocks.append(Block((Block.width * 9,SCREEN_HEIGHT*3/4 + Block.height * -6),self.collision_layer["none"],"LEAFS"))

        self.blocks.append(Block((Block.width * 11,SCREEN_HEIGHT*3/4 + Block.height * -3),self.collision_layer["none"],"LEAFS"))
        self.blocks.append(Block((Block.width * 11,SCREEN_HEIGHT*3/4 + Block.height * -4),self.collision_layer["none"],"LEAF"))
        self.blocks.append(Block((Block.width * 11,SCREEN_HEIGHT*3/4 + Block.height * -5),self.collision_layer["none"],"LEAFS"))
        # self.blocks.append(Block((Block.width * 11,SCREEN_HEIGHT*3/4 + Block.height * -6),self.collision_layer["none"],"LEAFS"))


        # self.blocks.append(Block((Block.width * 12,SCREEN_HEIGHT*3/4 + Block.height * -3),self.collision_layer["none"],"LEAFS"))
        # self.blocks.append(Block((Block.width * 12,SCREEN_HEIGHT*3/4 + Block.height * -4),self.collision_layer["none"],"LEAFS"))
        # self.blocks.append(Block((Block.width * 12,SCREEN_HEIGHT*3/4 + Block.height * -5),self.collision_layer["none"],"LEAFS"))
        # self.blocks.append(Block((Block.width * 8,SCREEN_HEIGHT*3/4 + Block.height * -3),self.collision_layer["none"],"LEAFS"))
        # self.blocks.append(Block((Block.width * 8,SCREEN_HEIGHT*3/4 + Block.height * -4),self.collision_layer["none"],"LEAFS"))
        # self.blocks.append(Block((Block.width * 8,SCREEN_HEIGHT*3/4 + Block.height * -5),self.collision_layer["none"],"LEAFS"))


    def update(self, delta):
        for block in self.blocks:
            block.update(delta)

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)
