from Setup import *
from Game import Game

scene = Game()

delta = 1000//fps
is_running = True
while is_running:
    screen.fill((255,255,255))

    if pg.event.peek(pg.QUIT, pump=True):
        is_running = False

    scene.update(delta)
    scene.draw(screen)

    pg.display.update()
    delta = clock.tick(fps)

pg.quit()