from Setup import *
from Game import Game
from Test import Test
from LevelCreator import LevelCreator
from MainMenu import Menu
from Function.Transition import TransitionScene

from DevLevelSelect import DevLevelSelect

delta = 1000//fps
is_running = True

# scene = Menu()
# scene = TransitionScene()
scene = DevLevelSelect()
old_level = 0
level = 0
next_level = 0

while is_running:
    if pg.event.peek(pg.QUIT):
        is_running = False

    if level == -1:
        level = old_level
        old_level = 0
    
    if old_level != level:
        match level:
            case -4:
                scene = TransitionScene(next_level)
            case -3:
                scene = DevLevelSelect()
            case -2:
                scene = LevelCreator()
            case 0:
                scene = Menu()
            case 1:
                scene = Game(1)
            case 2:
                scene = Game(2)
            case 3:
                scene = Game(3)
            case 4:
                scene = Game(4)
        old_level = level

    if level <= 1:
        level = scene.level
        try:
            next_level = scene.next_level
        except:
            next_level = 0

    scene.update(delta)
    scene.draw(screen)

    pg.display.update()
    delta = clock.tick(fps)

pg.quit()
