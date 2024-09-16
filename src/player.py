from entity import Ent
from input import Input
from object import Obj
from settings import Direction, SPEED, fvec2

class Player(Ent):
    def __init__(self, x_pos: float, y_pos: float):
        filepath = "../res/pc.png"
        animation_steps = 1
        self.velocity = fvec2(0, 0)
        self.selected_obj: Obj = None
        self.inventory = []
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

    def get_bottom_pos(self) -> fvec2:
        return fvec2(self.pos.x + self.size.x/2, self.pos.y + self.size.y - 10)

    def interact(self, room) -> None:
        if self.selected_obj != None:
            if self.selected_obj.obj_type == Obj_Type.pickup:
                self.inventory.append(self.selected_obj)
                for t in room.tiles:
                    if t.obj != None:
                        if self.selected_obj in t.obj:
                            t.obj.remove(self.selected_obj)
                self.selected_obj = None





        