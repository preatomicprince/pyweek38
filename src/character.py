from entity import Ent
from enum import Enum
from object import Obj, Obj_Type
from settings import SPEED, Direction, fvec2, TILE_W

Char = Enum("Char", ["heir", "duke", "duchess", "cleaner", "lady"])

class Character(Ent):
    def __init__(self, x_pos, y_pos, char: Char):
        self.char = char
        self.dir = Direction.dl
        self.dl_start = 0
        self.dr_start = 8
        self.ur_start = 16
        self.ul_start = 24

        self.current_room = 0
        animation_steps = 32

        
        self.next_tile: ind = 0
        
        match self.char:
            case Char.heir:
                self.path = [0]
                filepath = "../res/the_heir.png"

            case Char.duke:
                self.current_room = 3
                self.path = [0, 1, 2, 3]
                filepath = "../res/duke_sprite.png"

            case Char.duchess:
                self.path = [0]
                animation_steps = 4
                self.dr_start = 1
                self.ur_start = 2
                self.ul_start = 3
                filepath = "../res/mother.png"

            case Char.cleaner:
                self.path = [0]
                filepath = "../res/the_maid.png"

            case Char.lady:
                self.path = [0]
                animation_steps = 16
                self.dr_start = 4
                self.ur_start = 8
                self.ul_start = 12
                filepath = "../res/grandma.png"

        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, game_vars) -> None:

        self.sprites.update(game_vars.time)

        current_tile = game_vars.current_room.find_ent_tile(self)            

        if self.path[self.next_tile] == current_tile:
            if self.next_tile == len(self.path) - 1:
                self.path.reverse()
                self.next_tile = 0
            else:
                self.next_tile += 1

            if len(game_vars.room_list[self.current_room].tiles[current_tile].obj) > 0:
                for o in game_vars.room_list[self.current_room].tiles[current_tile].obj:
                    if o.obj_type == Obj_Type.door:
                        game_vars.room_list[self.current_room].chars.remove(self)
                        self.current_room = o.new_room
                        game_vars.room_list[self.current_room].chars.append(self)

                        self.pos.x = game_vars.room_list[o.new_room].tiles[o.go_to].pos.x + TILE_W/2
                        self.pos.y = game_vars.room_list[o.new_room].tiles[o.go_to].pos.y - self.size.y/2
            
            #simple back and forth. Needs updating
            if self.path[self.next_tile] > current_tile:
                self.dir = Direction.dl
            elif self.path[self.next_tile] < current_tile:
                self.dir = Direction.ur

            match self.dir:
                case Direction.dl:
                    self.vel = fvec2(-SPEED.x/2, SPEED.y/2)
                    self.sprites.set_animation(self.dl_start, self.dr_start - 1)

                case Direction.ur:
                    self.vel = fvec2(SPEED.x/2, -SPEED.y/2)
                    self.sprites.set_animation(self.ur_start, self.ul_start - 1)

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y


 
