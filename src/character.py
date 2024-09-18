from entity import Ent
from enum import Enum
from object import Obj, Obj_Type
from settings import SPEED, Direction, fvec2, TILE_W

Char = Enum("Char", ["heir", "duke", "duchess", "cleaner", "lady"])

class Character(Ent):
    def __init__(self, x_pos, y_pos, char: Char):
        self.char = char
        self.dir = Direction.dl

        # Start frame for each direction's walk cycle
        # End frame should be the next start minus 1
        self.dl_start = 0
        self.dr_start = 8
        self.ur_start = 16
        self.ul_start = 24

        # Room the character is in
        self.current_room = 0
        animation_steps = 32

        # Index for self.path[]
        self.next_tile: ind = 0

        # List of points the character will travel to. 
        # Each int represents the index for room.tiles[]
        # If a tile in path contains a door, the character will walk through when reached
        self.path: List(int) = []
        
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
                animation_steps = 21
                self.dr_start = 4
                self.ur_start = 8
                self.ul_start = 12
                filepath = "../res/grandma.png"

        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, game_vars) -> None:

        self.sprites.update(game_vars.time)

        current_tile = game_vars.room_list[self.current_room].find_ent_tile(self)            

        if self.path[self.next_tile] == current_tile:

            # If at end of path, reverse path and walk back along route
            # else set next target
            if self.next_tile == len(self.path) - 1:
                self.path.reverse()
                self.next_tile = 0
            else:
                self.next_tile += 1

            # When next tile reached, check if it has a door.
            if len(game_vars.room_list[self.current_room].tiles[current_tile].obj) > 0:
                for o in game_vars.room_list[self.current_room].tiles[current_tile].obj:
                    if o.obj_type == Obj_Type.door:

                        # Go through door
                        game_vars.room_list[self.current_room].chars.remove(self)
                        self.current_room = o.new_room
                        game_vars.room_list[self.current_room].chars.append(self)

                        self.pos.x = game_vars.room_list[o.new_room].tiles[o.go_to].pos.x + TILE_W/2
                        self.pos.y = game_vars.room_list[o.new_room].tiles[o.go_to].pos.y - self.size.y/2

            # Check tiles next to current tile
            # If interact object is active, kill character

            # List of nearby tiles
            above_tile = current_tile - 1
            below_tile = current_tile + 1
            left_tile = current_tile - game_vars.room_list[self.current_room].rows
            right_tile = current_tile + game_vars.room_list[self.current_room].rows

            check_tiles = [above_tile, below_tile, left_tile, right_tile]

            # Check tiles
            for t in check_tiles:
                if len(game_vars.room_list[self.current_room].tiles[t].obj) > 0:
                    for o in game_vars.room_list[self.current_room].tiles[t].obj:
                        if o.obj_type == Obj_Type.interact:
                            
                            # Kill character
                            if o.active == True:
                                self.alive = False

            
            # Simple back and forth. Direction.ur to Direction.dl. 
            # Needs updating to find tiles to left and right
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


 
