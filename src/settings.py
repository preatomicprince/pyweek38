from enum import Enum

class ivec2:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

class fvec2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class Settings:
    def __init__(self) -> None:
        self.running = True

# u = up, d = down, l = left, r = right
Direction = Enum('direction', ['u', 'ul', 'l', 'dl', 'd', 'dr', 'r', 'ur'])

WIDTH = 700
HEIGHT = 500
ISO_RATIO = 2 #tile_w/tile_h

_BASE_SPEED = 0.2
SPEED =  fvec2(_BASE_SPEED*ISO_RATIO, _BASE_SPEED)


