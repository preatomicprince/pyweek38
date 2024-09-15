from entity import Ent
from input import Input
from settings import SPEED

class Player(Ent):
    def __init__(self, x_pos: float, y_pos: float):
        filepath = "./res/pc.png"
        animation_steps = 1
        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, input: Input):
        if input.key_right:
            self.pos.x += SPEED.x

        if input.key_left:
            self.pos.x -= SPEED.x

        if input.key_up:
            self.pos.y -= SPEED.y

        if input.key_down:
            self.pos.y += SPEED.y
        
        