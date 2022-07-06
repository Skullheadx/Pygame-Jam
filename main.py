from Setup import *
from Game import Game

scene = Game()

delta = 1000//fps
is_running = True
while is_running:
    if pg.event.peek(pg.QUIT):
        is_running = False

    scene.update(delta)
    scene.draw(screen)

    pg.display.update()
    delta = clock.tick(fps)

pg.quit()
