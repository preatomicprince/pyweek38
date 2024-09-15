from entity import Ent

class Obj(Ent):
    def __init__(self, x_pos: float, y_pos: float, filepath: str, animation_steps = 1, collide = True, interact = False):
        self.collide: bool = collide
        self.interact = True
        super().__init__(x_pos, y_pos, filepath, animation_steps)
