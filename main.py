from typing import Final
from Setup import *
import Setup
from Game import Game
from Test import Test
from LevelCreator import LevelCreator
from MainMenu import Menu
from Function.Transition import TransitionScene
from UI.FinalScreen import FinalScreen
from UI.Credits import Credits

from DevLevelSelect import DevLevelSelect

delta = 1000//fps
# scene = Menu()
# scene = TransitionScene()
scene = Menu()
old_level = 0
level = 4
next_level = 0

# final_level = 6

while Setup.is_running:
    if pg.event.peek(pg.QUIT):
        Setup.is_running = False

    if level == -1:
        level = old_level
        old_level = 0

    if old_level != level:
        match level:
            case -5:
                scene = Credits()
            case -4:
                scene = TransitionScene(next_level)
            case -3:
                scene = DevLevelSelect()
            case -2:
                scene = LevelCreator()
            case 0:
                scene = Menu()
            case 5:
                scene = FinalScreen()
            case _:
                scene = Game(level)
        old_level = level

    level = scene.level
    try:
        next_level = scene.next_level
    except:
        next_level = 0

    scene.update(delta)
    scene.draw(screen)

    pg.display.update()
    delta = clock.tick(fps)
    # print(clock.get_fps())

pg.quit()
