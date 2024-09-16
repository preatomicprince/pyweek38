from entity import Ent
from enum import Enum
from settings import TILE_H

Obj_Type = Enum("Obj_type", ["wall", "door", "other"])


class Obj(Ent):
    def __init__(self, filepath: str, animation_steps: int = 1, ind: int = 0, obj_type: Obj_Type = Obj_Type.other):
        self.obj_type = obj_type
        self.go_to = None
        self.selected = False

        match self.obj_type:
            case Obj_Type.wall:
                self.collide = False
                self.interact = False

            case Obj_Type.door:
                self.collide = False
                self.interact = True
                self.go_to = "dining"

            case Obj_Type.other:
                self.collide = True
                self.interact = False
        
        
        x_pos = 0
        y_pos = 0
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)
