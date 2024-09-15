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
Direction = Enum('direction', ['u', 'ul', 'l', 'dl', 'd', 'dr', 'r', 'ur']) 


