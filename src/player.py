from entity import Ent
from input import Input
from settings import Direction, SPEED, fvec2

class Player(Ent):
    def __init__(self, x_pos: float, y_pos: float):
        filepath = "../res/pc.png"
        animation_steps = 1
        self.velocity = fvec2(0, 0)
        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, input: Input):
        self.velocity = fvec2(0, 0)

        if input.key_right:
            self.dir = Direction.dr

        if input.key_left:
            self.dir = Direction.ul

        if input.key_up:
            self.dir = Direction.ur

        if input.key_down:
            self.dir = Direction.dl

        match self.dir:
            case Direction.dr:
                self.velocity.x += SPEED.x
                self.velocity.y += SPEED.y

            case Direction.ul:
                self.velocity.x -= SPEED.x
                self.velocity.y -= SPEED.y

            case Direction.ur:
                self.velocity.x += SPEED.x
                self.velocity.y -= SPEED.y

            case Direction.dl:
                self.velocity.x -= SPEED.x
                self.velocity.y += SPEED.y

     
        if input.key_right or input.key_left or input.key_up or input.key_down:
            self.pos.x += self.velocity.x
            self.pos.y += self.velocity.y

        