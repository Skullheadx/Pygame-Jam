from Setup import *
from Game import Game
from MainMenu import Menu

delta = 1000//fps
is_running = True

level = 1
old_level = level
# scene = Menu()

scene = Game()

while is_running:
    if pg.event.peek(pg.QUIT):
        is_running = False

    if level == 0:
        level = scene.level

    if old_level != level:
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
