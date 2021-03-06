import os
import numpy as np

from Function.createText import createText
from Setup import *

import tkinter as tk
from tkinter import filedialog


class LevelCreator:
    canvas_layers = 5
    textures = [file[:file.index(".")] for file in listdir("Assets/world/blocks")]
    textures.append("NONE")
    for file in listdir("Assets/world/decor"):
        textures.append(file[:file.index(".")])

    def __init__(self):
        self.mode = "MOVE"
        self.pos1 = pg.Vector2(0,0)
        self.pos2 = pg.Vector2(0,0)

        self.blocks = {"none": [[] for _ in range(self.canvas_layers)],
                       "world": [[] for _ in range(self.canvas_layers)]}

        self.grid = Grid()

        self.zoom = 1
        self.total_offset = pg.Vector2(0, 0)
        self.world_transform = np.identity(3)
        self.inv_world_transform = np.linalg.inv(self.world_transform)

        self.translation_matrix = np.array([[1, 0, self.total_offset.x],
                                            [0, 1, self.total_offset.y],
                                            [0, 0, 1]])
        self.translation_back_matrix = np.array([[1, 0, -self.total_offset.x],
                                                 [0, 1, -self.total_offset.y],
                                                 [0, 0, 1]])

        self.current_texture = self.textures.index("PLACEHOLDER")
        self.current_layer = 0
        self.show_grid = True
        self.show_hitboxes = False
        self.collision_layer = "world"

        self.buttons = [Button((0, 0), "Toggle Grid", self.toggle_grid),
                        Button((0, 0), "-Layer", self.decrease_layer),
                        Button((0, 0), f"{self.current_layer=}", self.upd_layer),
                        Button((0, 0), "+Layer", self.increase_layer),
                        Button((0, 0), f"{self.collision_layer=}", self.toggle_collidable),
                        Button((0, 0), "Toggle Hitboxes", self.toggle_show_hitboxes),
                        Button((0, 0), "Import", self.import_level),
                        Button((0, 0), "Export", self.export),
                        ]

        self.level = -2

        self.select = False

        self.boxes = []
        x=0
        y=0
        for i, img in enumerate(self.textures):
            if x + i * 50 >= SCREEN_WIDTH-50:
                x = - i * 50
                y += 50
            self.boxes.append(Icon((x + i * 50, y), img))

    def export(self):
        # for layer in out:
        #     for i,block in enumerate(layer):
        #         layer[i] = Block(block.position,block.collision_layer,block.texture_name)

        counter = 1

        def get_key(mask):
            for key, value in self.blocks.items():
                if mask == value:
                    return key

        while True:
            try:
                with open(os.path.join("Levels", f'Level{counter}.txt'), 'x') as f:
                    out = ""
                    for layer in self.get_canvas_layers():
                        t = ""
                        pos = ""
                        texture = ""
                        for block in layer:
                            t += f"{get_key(block.collision_layer)}|"
                            pos += f"{block.position.x},{block.position.y}|"
                            texture += f"{block.texture_name}|"
                        out += f"{t[:-1]}\n{pos[:-1]}\n{texture[:-1]}\n"
                    f.write(out)

                print(f"File saved as Level{counter} in folder Levels")
                break
            except FileExistsError:
                counter += 1

    def import_level(self):
        root = tk.Tk()
        root.withdraw()

        filename = filedialog.askopenfilename(initialdir="./Levels", title="Select A File",
                                              filetypes=((".txt", "*.txt"), ("all files", "*.*")))
        if filename == '':
            return
        with open(filename, 'r', encoding='utf-8') as f:
            file_contents = f.read().split("\n")

        # with open(path.join("Levels", f'Level{1}.txt'), 'r') as f:
        #     file_contents = f.read().split("\n")

        for i in range(0, len(file_contents) - 1, 3):
            layer = file_contents[i].split("|")
            pos = file_contents[i + 1].split("|")
            texture = file_contents[i + 2].split("|")

            for l, p, t in zip(layer, pos, texture):
                if p == "":
                    break
                x, y = p.split(',')
                self.add_block(self.apply_transformations((float(x), float(y))), self.blocks[l], t, i//3)

    def toggle_collidable(self):
        if self.collision_layer == "none":
            self.collision_layer = "world"
        else:
            self.collision_layer = "none"
        button = self.buttons[4]
        button.upd_text(button.position, f"{self.collision_layer=}")

    def toggle_show_hitboxes(self):
        self.show_hitboxes = not self.show_hitboxes

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def decrease_layer(self):
        self.current_layer = max(self.current_layer - 1, 0)
        self.upd_layer()

    def increase_layer(self):
        self.current_layer = min(self.current_layer + 1, self.canvas_layers - 1)
        self.upd_layer()

    def upd_layer(self):
        button = self.buttons[2]
        button.__init__(button.position, f"{self.current_layer=}", self.upd_layer)

    def fit_to_grid(self, pt, use_floor=True):
        pos = self.reverse_transformations(pg.Vector2(pt))
        if use_floor:
            return pg.Vector2((pos.x // EditorBlock.width) * EditorBlock.width,
                              (pos.y // EditorBlock.height) * EditorBlock.height)
        else:
            return pg.Vector2(round(pos.x / EditorBlock.width) * EditorBlock.width,
                              round(pos.y / EditorBlock.height) * EditorBlock.height)

    def apply_rect_transformations(self, rect):
        top_left = np.array([rect.left, rect.top, 1])
        bottom_right = np.array([rect.right, rect.bottom, 1])

        top_left = pg.Vector2(tuple((self.world_transform @ self.translation_matrix @ top_left)[0:2]))
        bottom_right = pg.Vector2(tuple((self.world_transform @ self.translation_matrix @ bottom_right)[0:2]))

        return pg.Rect(top_left, bottom_right - top_left)

    def add_block(self, pos, mask, texture, canvas_layer):
        pos = self.fit_to_grid(pos)
        for m in self.blocks.values():
            for i, block in enumerate(m[canvas_layer]):
                if block.position == pos:
                    del m[canvas_layer][i]
                    break
        if texture != "NONE":
            mask[canvas_layer].append(EditorBlock(pos, mask, texture))

    def calculate_transformations(self, current_frame_zoom):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())

        translation_matrix = np.array([[1, 0, mouse_pos.x],
                                       [0, 1, mouse_pos.y],
                                       [0, 0, 1]])
        translation_back_matrix = np.array([[1, 0, -mouse_pos.x],
                                            [0, 1, -mouse_pos.y],
                                            [0, 0, 1]])
        scale_matrix = np.array([[current_frame_zoom, 0, 0],
                                 [0, current_frame_zoom, 0],
                                 [0, 0, 1]])
        self.world_transform = translation_matrix @ scale_matrix @ translation_back_matrix @ self.world_transform
        self.inv_world_transform = np.linalg.inv(self.world_transform)

    def apply_transformations(self, pt):
        point = pg.Vector2(pt)
        point = np.array([point.x, point.y, 1])
        return pg.Vector2(tuple((self.world_transform @ self.translation_matrix @ point)[0:2]))

    def reverse_transformations(self, pt):
        point = pg.Vector2(pt)
        point = np.array([point.x, point.y, 1])
        return pg.Vector2(tuple((self.translation_back_matrix @ self.inv_world_transform @ point)[0:2]))

    def update(self, delta):
        if self.select:
            for ev in pg.event.get(pg.KEYUP):
                if ev.key == pg.K_f:
                    self.select = False


            for i in self.boxes:
                temp = i.update(delta)
                if temp is not None:
                    self.current_texture = self.textures.index(temp)
                    self.select = False
            return

        current_frame_zoom = 1
        for event in pg.event.get((pg.MOUSEBUTTONDOWN, pg.MOUSEWHEEL, pg.KEYUP)):
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pg.key.get_pressed()[pg.K_LSHIFT]:
                        self.mode = "SELECT"
                        self.pos1 = self.fit_to_grid(pg.mouse.get_pos(), True)
                    else:
                        self.mode = "MOVE"
                        pg.mouse.get_rel()
                elif event.button == 3:
                    if self.mode == "SELECT":
                        pg.mouse.get_rel()
            if event.type == pg.MOUSEWHEEL:
                if event.y < 0:
                    current_frame_zoom *= 0.75
                    self.zoom *= 0.75
                elif event.y > 0:
                    current_frame_zoom *= 1.25
                    self.zoom *= 1.25
            if event.type == pg.KEYUP:
                if event.key in [pg.K_a, pg.K_s, pg.K_LEFT, pg.K_DOWN]:
                    self.current_texture = (self.current_texture - 1) % len(self.textures)
                elif event.key in [pg.K_d, pg.K_w, pg.K_RIGHT, pg.K_UP]:
                    self.current_texture = (self.current_texture + 1) % len(self.textures)
                elif event.key == pg.K_f:
                    self.select = True

        mouse_pressed = pg.mouse.get_pressed(3)
        if mouse_pressed[0]:
            if self.mode == "MOVE":
                mouse_rel = pg.mouse.get_rel()
                self.total_offset += pg.Vector2(mouse_rel[0] / self.zoom, mouse_rel[1] / self.zoom)
            elif self.mode == "SELECT":
                self.pos2 = self.fit_to_grid(pg.mouse.get_pos(), True)
        if mouse_pressed[2]:
            if self.mode == "SELECT":
                mouse_rel = pg.Vector2(pg.mouse.get_rel())
                self.pos1 += mouse_rel
                self.pos2 += mouse_rel
                # self.pos2 = self.fit_to_grid(self.pos2)
                # for mask in self.blocks.values():
                #     for layer in mask:
                #         for block in layer:
                #             block.position
            elif self.mode == "MOVE":
                self.add_block(pg.mouse.get_pos(), self.blocks[self.collision_layer], self.textures[self.current_texture],
                           self.current_layer)

        self.translation_matrix = np.array([[1, 0, self.total_offset.x],
                                            [0, 1, self.total_offset.y],
                                            [0, 0, 1]])
        self.translation_back_matrix = np.array([[1, 0, -self.total_offset.x],
                                                 [0, 1, -self.total_offset.y],
                                                 [0, 0, 1]])

        self.calculate_transformations(current_frame_zoom)

        self.grid.update(delta, self.world_transform, self.inv_world_transform, self.total_offset, self.zoom)

        for mask in self.blocks.values():
            for layer in mask:
                for block in layer:
                    block.update(delta, self.world_transform, self.total_offset)

        prev_x = 0
        for button in self.buttons:
            button.update(delta, dx=prev_x)
            prev_x += button.width + 10

    def get_canvas_layers(self):
        out = [[] for _ in range(self.canvas_layers)]
        for mask in self.blocks.values():
            for i, layer in enumerate(mask):
                out[i] += layer
        return out

    def draw(self, surf):
        surf.fill((0, 0, 0))
        if self.select:
            for i in self.boxes:
                i.draw(surf)
            return

        if self.show_grid:
            self.grid.draw(surf)

        for i, layer in enumerate(self.get_canvas_layers()):
            if i <= self.current_layer:
                for block in layer:
                    block.draw(surf)
                    if self.show_hitboxes:
                        block.show_hitbox(surf, self.blocks["world"])

        pg.draw.line(surf, (255, 0, 0), self.apply_transformations((self.reverse_transformations((0, 0)).x, 0)),
                     self.apply_transformations((self.reverse_transformations((SCREEN_WIDTH, 0)).x, 0)),
                     math.ceil(self.zoom * 5))
        pg.draw.line(surf, (255, 0, 0), self.apply_transformations((0, self.reverse_transformations((0, 0)).y)),
                     self.apply_transformations((0, self.reverse_transformations((0, SCREEN_HEIGHT)).y)),
                     math.ceil(self.zoom * 5))

        display_img = EditorBlock.textures[self.textures[self.current_texture]].copy()
        display_img.set_alpha(200)
        surf.blit(pg.transform.scale(display_img, self.apply_rect_transformations(display_img.get_rect()).size),
                  self.apply_transformations(self.fit_to_grid(pg.mouse.get_pos(), use_floor=True)))

        if self.mode == "SELECT":
            pg.draw.rect(surf,(255,0,0),self.apply_rect_transformations(pg.Rect(self.pos1, self.pos2-self.pos1)),3)

        for button in self.buttons:
            button.draw(surf)



class Grid:
    thickness = 2
    colour = (100, 100, 100)

    def __init__(self):
        self.zoom = 1
        self.world_transform = np.identity(3)
        self.inv_world_transform = np.linalg.inv(self.world_transform)
        self.total_offset = pg.Vector2(0, 0)
        self.translation_matrix = np.array([[1, 0, self.total_offset.x],
                                            [0, 1, self.total_offset.y],
                                            [0, 0, 1]])
        self.translation_back_matrix = np.array([[1, 0, -self.total_offset.x],
                                                 [0, 1, -self.total_offset.y],
                                                 [0, 0, 1]])

    def update(self, delta, world_transform, inv_world_transform, total_offset, zoom):
        self.zoom = zoom
        self.world_transform = world_transform
        self.inv_world_transform = inv_world_transform
        self.total_offset = total_offset
        self.translation_matrix = np.array([[1, 0, self.total_offset.x],
                                            [0, 1, self.total_offset.y],
                                            [0, 0, 1]])
        self.translation_back_matrix = np.array([[1, 0, -self.total_offset.x],
                                                 [0, 1, -self.total_offset.y],
                                                 [0, 0, 1]])

    def apply_transformations(self, pt):
        point = pg.Vector2(pt)
        point = np.array([point.x, point.y, 1])
        return pg.Vector2(tuple((self.world_transform @ self.translation_matrix @ point)[0:2]))

    def reverse_transformations(self, pt):
        point = pg.Vector2(pt)
        point = np.array([point.x, point.y, 1])
        return pg.Vector2(tuple((self.translation_back_matrix @ self.inv_world_transform @ point)[0:2]))

    def draw(self, surf):
        start = self.reverse_transformations((0, 0))
        end = self.reverse_transformations(dimensions)

        start = pg.Vector2(start.x // EditorBlock.width, start.y // EditorBlock.width)
        end = pg.Vector2(end.x // EditorBlock.height, end.y // EditorBlock.height)

        for i in range(math.floor(start.x), math.floor(end.x) + 1):
            pg.draw.line(surf, self.colour,
                         self.apply_transformations((i * EditorBlock.width, start.y * EditorBlock.height)),
                         self.apply_transformations((i * EditorBlock.width, (end.y + 1) * EditorBlock.height)),
                         math.ceil(self.thickness * self.zoom))
        for i in range(math.floor(start.y), math.floor(end.y) + 1):
            pg.draw.line(surf, self.colour,
                         self.apply_transformations((start.x * EditorBlock.width, i * EditorBlock.height)),
                         self.apply_transformations(((end.x + 1) * EditorBlock.width, i * EditorBlock.height)),
                         math.ceil(self.thickness * self.zoom))


class EditorBlock:
    textures = {file[:file.index(".")]: pg.transform.scale(
        pg.image.load(path.join("Assets/world/blocks", file)), (50, 50)) for
        file in listdir("Assets/world/blocks")}
    for file in listdir("Assets/world/decor"):
        textures[file[:file.index(".")]] = pg.transform.scale(
            pg.image.load(path.join("Assets/world/decor", file)), (50, 50))
    width, height = textures["PLACEHOLDER"].get_size()

    def __init__(self, pos, collision_layer, texture="PLACEHOLDER"):
        self.position = pg.Vector2(pos)
        self.texture = self.textures[texture]
        self.texture_name = texture

        self.collision_layer = collision_layer

        self.world_transform = np.identity(3)
        self.total_offset = pg.Vector2(0, 0)
        self.translation_matrix = np.array([[1, 0, self.total_offset.x],
                                            [0, 1, self.total_offset.y],
                                            [0, 0, 1]])

    def update(self, delta, world_transform, total_offset):
        self.world_transform = world_transform
        self.total_offset = total_offset
        self.translation_matrix = np.array([[1, 0, self.total_offset.x],
                                            [0, 1, self.total_offset.y],
                                            [0, 0, 1]])

    def apply_transformations(self, rect):
        top_left = np.array([rect.left, rect.top, 1])
        bottom_right = np.array([rect.right, rect.bottom, 1])

        top_left = pg.Vector2(tuple((self.world_transform @ self.translation_matrix @ top_left)[0:2]))
        bottom_right = pg.Vector2(tuple((self.world_transform @ self.translation_matrix @ bottom_right)[0:2]))

        return pg.Rect(top_left, bottom_right - top_left)

    def get_display_rect(self):
        return self.apply_transformations(pg.Rect(self.position, (self.width, self.height)))

    def draw(self, surf):
        display_rect = self.get_display_rect()
        if display_rect.colliderect(screen_rect):
            surf.blit(pg.transform.scale(self.texture, display_rect.size), display_rect)

    def show_hitbox(self, surf, collision_layer):
        if collision_layer == self.collision_layer:
            pg.draw.rect(surf, (255, 0, 0), self.get_display_rect(), 3)


class Button:

    def __init__(self, pos, msg, func):
        self.position = pg.Vector2(pos)
        self.text, self.rect = createText(self.position.x * 2, self.position.y, 20, (200, 200, 200), "Regular", msg)
        self.width, self.height = self.text.get_size()
        self.func = func
        self.msg = msg
        self.cooldown = 500

    def upd_text(self, pos, msg):
        self.position = pg.Vector2(pos)
        self.text, self.rect = createText(self.position.x * 2, self.position.y, 20, (200, 200, 200), "Regular", msg)
        self.width, self.height = self.text.get_size()
        self.msg = msg

    def update(self, delta, dx):
        self.upd_text((dx, self.position.y), self.msg)
        mouse_pos = pg.mouse.get_pos()
        if self.cooldown == 0:
            if pg.mouse.get_pressed(3)[0]:
                if (self.position.x <= mouse_pos[0] <= self.position.x + self.width and
                        self.position.y <= mouse_pos[1] <= self.position.y + self.height):
                    self.func()
                    self.cooldown = 500
        self.cooldown = max(self.cooldown - delta, 0)

    def draw(self, surf):
        pg.draw.rect(surf, (80, 80, 80), pg.Rect(self.position, self.text.get_size()), border_radius=3)
        pg.draw.rect(surf, (120, 120, 120), pg.Rect(self.position, self.text.get_size()), 1, border_radius=3)
        surf.blit(self.text, self.rect)


class Icon:
    textures = {file[:file.index(".")]: pg.transform.scale(
        pg.image.load(path.join("Assets/world/blocks", file)), (50, 50)) for
        file in listdir("Assets/world/blocks")}
    for file in listdir("Assets/world/decor"):
        textures[file[:file.index(".")]] = pg.transform.scale(
            pg.image.load(path.join("Assets/world/decor", file)), (50, 50))
    width, height = textures["PLACEHOLDER"].get_size()

    def __init__(self, pos, img):
        self.position = pg.Vector2(pos)
        self.img = img
        self.display_img = self.textures[self.img]
        self.width, self.height = self.display_img.get_size()
        self.rect = pg.Rect(self.position, (self.width, self.height))
        self.show_outline = False

    def update(self, delta):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.show_outline = True
            if pg.mouse.get_pressed(3)[0]:
                return self.img
        else:
            self.show_outline = False
        return None

    def draw(self, surf):
        surf.blit(self.display_img, self.position)
        if self.show_outline:
            pg.draw.rect(surf, (255, 0, 0), self.rect, 3)
