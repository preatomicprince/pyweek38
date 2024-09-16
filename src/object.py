from entity import Ent
from enum import Enum
from settings import TILE_H

Obj_Type = Enum(Obj_type, [wall, other]


class Obj(Ent):
    def __init__(self, filepath: str, animation_steps: int = 1, collide: bool = True, interact = False, ind: int = 0, obj_type: Obj_Type = Obj_Type.other):
        self.collide = collide
        self.interact = interact
        self.obj_type = obj_type
        x_pos = 0
        y_pos = 0
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)
