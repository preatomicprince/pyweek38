from entity import Ent
from enum import Enum
from object import Obj, Obj_Type
from pathing import Path_Tile, Pathing
from settings import SPEED, Direction, fvec2, TILE_W

Char = Enum("Char", ["heir", "duke", "duchess", "cleaner", "lady"])

class Character(Ent):
    def __init__(self, x_pos, y_pos, char: Char):
        self.char = char
        
        self.dir = Direction.dl
        self.prev_dir = Direction.ul
        
        

        # Start frame for each direction's walk cycle
        # End frame should be the next start minus 1
        self.dl_start = 0
        self.dr_start = 8
        self.ur_start = 16
        self.ul_start = 24

        # Room the character is in
        self.current_room = 0
        self.walking_animation_steps = 32

        self.pathing = Pathing()

        # List of points the character will travel to. 
        # Each int represents the index for room.tiles[]
        # If a tile in path contains a door, the character will walk through when reached
        self.path: list = []
        
        self.alive = True

        match self.char:
            case Char.heir:
                animation_steps = 34
                self.current_room = 3
                self.path = [0]
                filepath = "../res/the_heir.png"

            case Char.duke:
                animation_steps = 39
                self.current_room = 3
                self.path = [0, 1, 2, 3]
                filepath = "../res/duke_sprite.png"

            case Char.duchess:
                self.current_room = 3
                self.path = [4, 5, 6, 7]
                self.walking_animation_steps = 4
                animation_steps = 9
                self.dr_start = 1
                self.ur_start = 2
                self.ul_start = 3
                filepath = "../res/mother.png"

            case Char.cleaner:
                animation_steps = 37
                self.current_room = 3
                self.path = [8, 10]
                filepath = "../res/the_maid.png"

            case Char.lady:
                self.current_room = 3
                self.path = [12, 15]
                self.walking_animation_steps = 16
                animation_steps = 21
                self.dr_start = 4
                self.ur_start = 8
                self.ul_start = 12
                filepath = "../res/grandma.png"

        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, game_vars) -> None:

        self.sprites.update(game_vars.time)

        self.pathing.update(game_vars, self)

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y


 
