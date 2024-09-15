from entity import Ent
from input import Input
from settings import SPEED, fvec2

class Player(Ent):
    def __init__(self, x_pos: float, y_pos: float):
        filepath = "./res/pc.png"
        animation_steps = 1
        self.velocity = fvec2(0, 0)
        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, input: Input):
        self.velocity = fvec2(0, 0)

        if input.key_right:
            self.velocity.x += SPEED.x

        if input.key_left:
            self.velocity.x -= SPEED.x

        if input.key_up:
            self.velocity.y -= SPEED.y

        if input.key_down:
            self.velocity.y += SPEED.y

        if self.velocity.x > 1:
            if self.velocity.y > 1:
                self.direction = 1
            elif self.velocity.y < 1:
                self.direction = 1
            elif self.velocity.y == 0:
                pass

        elif self.velocity.x < 1:
            if self.velocity.y > 1:
                pass
            elif self.velocity.y < 1:
                pass
            elif self.velocity.y == 0:
                pass

        elif self.velocity.x == 0:
            if self.velocity.y > 1:
                pass
            elif self.velocity.y < 1:
                pass
            elif self.velocity.y == 0:
                pass

        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

        