from entity import Ent
from object import Obj

class Tile(Ent):
    def __init__(self, x_pos: float, y_pos: float, obj: Obj = None):
        filepath = "./res/tile1.png"
        animation_steps = 1
        self.obj = obj
        super().__init__(x_pos, y_pos, filepath, animation_steps)