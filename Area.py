from Setup import *

areas = set()
def do_nothing(node): # placeholder func
    pass


class Area:

    def __init__(self, pos,offset, width ,height, target_node_type, func=do_nothing):
        self.position = pg.Vector2(pos)
        self.offset = pg.Vector2(offset)
        self.width = width
        self.height = height
        self.target = target_node_type
        self.func = func
        global areas
        areas.add(self)


    def update(self, delta, pos):
        self.position = pos

    def is_colliding(self,node):
        if isinstance(node, self.target):
            if self.get_collision_rect().colliderect(node.get_collision_rect()):
                return True
        return False

    def set_func(self, func):
        self.func = func

    def signal(self, node):
        self.func(node)

    def get_collision_rect(self):
        return pg.Rect(self.position + self.offset, (self.width, self.height))

    def draw(self, surf):
        pg.draw.rect(surf, (255,0,0),get_display_rect(self.get_collision_rect()))
