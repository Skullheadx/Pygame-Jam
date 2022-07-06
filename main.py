from Setup import *
from Game import Game
from Menu import Menu

delta = 1000//fps
is_running = True

level = 0
old_level = level
scene = Menu()

while is_running:
    if pg.event.peek(pg.QUIT):
        is_running = False

    if(level == 0):
        level = scene.level

    if(old_level != level):
        old_level = level
        match level:
            case 0:
                scene = Menu()
            case 1:
                scene = Game()

    scene.update(delta)
    scene.draw(screen)

    pg.display.update()
    delta = clock.tick(fps)

pg.quit()