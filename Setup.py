import pygame as pg
import math

import pygame.transform

from Area import Area

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 640
dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)
center = pg.Vector2(dimensions) / 2

pg.display.set_caption("Jam")
# icon = pg.transform.scale(pg.image.load("logo.ico"), (32, 32))
# pg.display.set_icon(icon)

clock = pg.time.Clock()
fps = 60

screen = pg.display.set_mode(dimensions, pg.SCALED)


def rotate(pos, img, angle, pivot):
    vec = (pos - pivot).rotate(-angle) + pivot
    rot_img = pg.transform.rotozoom(img, angle, 1)
    rot_rect = rot_img.get_rect(center=vec)
    return rot_img, rot_rect

camera_offset = center.copy()

MAP_WIDTH, MAP_HEIGHT = 10000,10000

def get_display_rect(collision_rect):
    camera_offset.x = max(0, min(camera_offset.x, MAP_WIDTH - SCREEN_WIDTH))
    camera_offset.y = max(0, min(camera_offset.y, MAP_HEIGHT - SCREEN_HEIGHT))

    pos = collision_rect.topleft
    width, height = collision_rect.w, collision_rect.h
    return pg.Rect(pos - camera_offset, (width, height))
<<<<<<< Updated upstream
=======
    # return pg.Rect(pos, (width, height))

def get_display_point(vec):
    camera_offset.x = max(0, min(camera_offset.x, MAP_WIDTH - SCREEN_WIDTH))
    camera_offset.y = max(0, min(camera_offset.y, MAP_HEIGHT - SCREEN_HEIGHT))
    return vec - camera_offset

from Area import Area
>>>>>>> Stashed changes
