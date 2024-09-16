from entity import Ent
from settings import TILE_H

class Obj(Ent):
    def __init__(self, filepath: str, animation_steps: int = 1, collide: bool = True, interact = False, ind: int = 0):
        self.collide = collide
        self.interact = interact
        x_pos = 0
        y_pos = 0
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)
