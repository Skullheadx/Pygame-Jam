from Setup import *
from Game import Game
from Test import Test
from MainMenu import Menu

delta = 1000//fps
is_running = True

scene = Menu()
old_level = 0


level = 1

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
