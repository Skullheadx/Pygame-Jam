import pygame as pg
import math
import random
from os import listdir, path


pg.init()

display_info = pg.display.Info()

SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 640
# SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h-10
dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)
center = pg.Vector2(dimensions) / 2

screen_rect = pg.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

pg.display.set_caption("Jam")
# icon = pg.transform.scale(pg.image.load("logo.ico"), (32, 32))
# pg.display.set_icon(icon)

clock = pg.time.Clock()
fps = 60
screen = pg.display.set_mode(dimensions, pg.SCALED)

is_running = True


def rotate(pos, img, angle, pivot):
    vec = (pos - pivot).rotate(-angle) + pivot
    rot_img = pg.transform.rotozoom(img, angle, 1)
    rot_rect = rot_img.get_rect(center=vec)
    return rot_img, rot_rect

camera_offset = center.copy()

MAP_WIDTH, MAP_HEIGHT = 250000,250000


def get_display_rect(collision_rect):
    pos = collision_rect.topleft
    width, height = collision_rect.w, collision_rect.h
    return pg.Rect(pos - camera_offset, (width, height))

def get_display_point(vec):
    return vec - camera_offset

def get_camera_offset():
    return camera_offset

from Area import Area

from PIL import Image

FORMAT = "RGBA"

def pil_to_game(img):
    data = img.tobytes("raw", FORMAT)
    return pg.image.fromstring(data, img.size, FORMAT)

def get_gif_frame(img, frame):
    img.seek(frame)
    return img.convert(FORMAT)

particles = []
