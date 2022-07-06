import pygame as pg
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

