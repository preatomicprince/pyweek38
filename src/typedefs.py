from enum import Enum

class ivec2:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

class fvec2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

# u = up, d = down, l = left, r = right
Direction = Enum('Direction', ['ul', 'dl', 'dr', 'ur'])

WIDTH = 900
HEIGHT = 700

TILE_W = 128
TILE_H = 64

ISO_RATIO = TILE_W/TILE_H

_BASE_SPEED = 70
SPEED =  fvec2(_BASE_SPEED*ISO_RATIO, _BASE_SPEED)