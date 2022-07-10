from Setup import *

def getWorldCoords(X, Y):
    coords = get_display_rect(pg.Rect(X, Y, 0, 0))
    coordsList = list(coords.topleft)

    return coordsList