import pygame as pg


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


delta = 1000//fps

is_running = True
while is_running:
    screen.fill((255,255,255))

    if pg.event.peek(pg.QUIT, pump=True):
        is_running = False

    pg.display.update()
    delta = clock.tick(fps)

pg.quit()