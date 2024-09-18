from object import Obj_Type
from settings import GameVars, ivec2, fvec2, Direction, SPEED

class Path_Tile:
    def __init__(self, room: int, tile: int,
                 door: bool = False, interaction: bool = False) -> None:
        
        #index of room in room_list[]
        self.room = room
        #index of tile in room.tiles[]
        self.tile = tile
        
        # If True, check for door on tile and walk through
        self.door = door

        # If true, interact with object on adjacent tile
        self.interaction = interaction        

class Pathing:
    def __init__(self, key_points = None, path_tiles = None) -> None:

        # All major stops and key interaction tiles
        # List of Path_Tiles
        self.key_points: list = [Path_Tile(3, 0), Path_Tile(3, 3, door = True)]

        # All stops between key points
        # List of tile indexes (int)
        # Should contain (len(self.key_points) - 1) lists
        # First in each list should be current key point. Last should be next key point
        self.path_tiles: list = [[0, 1, 2, 3]]

        # Index for room_list
        self.current_room = 3
        self.current_tile = self.path_tiles[0][0]
        
        # Indexes in self.path_list
        self.next_tile_ind = 1

        # Indexes in self.key_points
        self.current_key_point_ind = 0
        self.next_key_point_ind = 1

    def _reverse_path(self) -> None:
        # Reverses path so character traverses back to start

        self.key_points.reverse()

        for i in self.path_tiles:
            i.reverse()

        self.path_tiles.reverse()

    def _set_direction(self, game_vars, character):

        char_tile_coord = game_vars.room_list[self.current_room].ind_to_coord(self.current_tile)

        next_tile = self.path_tiles[self.current_key_point_ind][self.next_tile_ind]
        next_tile_coord = game_vars.room_list[self.current_room].ind_to_coord(next_tile)

        character.prev_dir = character.dir

        if next_tile_coord.x > char_tile_coord.x:
            character.dir = Direction.dr
        elif next_tile_coord.x < char_tile_coord.x:
            character.dir = Direction.ul
        elif next_tile_coord.y > char_tile_coord.y:
            character.dir = Direction.dl
        elif next_tile_coord.y < char_tile_coord.y: 
            character.dir = Direction.ur

        if character.dir != character.prev_dir:

            match character.dir:
                case Direction.dl:
                    character.vel = fvec2(-SPEED.x/2, SPEED.y/2)
                    character.sprites.set_animation(character.dl_start, character.dr_start - 1)

                case Direction.ur:
                    character.vel = fvec2(SPEED.x/2, -SPEED.y/2)
                    character.sprites.set_animation(character.ur_start, character.ul_start - 1)

                case Direction.ul:
                    character.vel = fvec2(-SPEED.x/2, -SPEED.y/2)
                    character.sprites.set_animation(character.ul_start, character.walking_animation_steps - 1)

                case Direction.dr:
                    character.vel = fvec2(SPEED.x/2, SPEED.y/2)
                    character.sprites.set_animation(character.dr_start, character.ur_start - 1)

    def update(self, game_vars, character):
        self.current_tile = game_vars.room_list[self.current_room].find_ent_tile(character)

        next_tile = self.path_tiles[self.current_key_point_ind][self.next_tile_ind]
        next_key_point = self.key_points[self.next_key_point_ind].tile

        if self.current_tile == next_tile:
            print(self.current_tile)
            if self.current_tile == next_key_point:
                print(f"key point: {next_key_point}")
                self.current_tile = 0
                self.next_tile_ind = 1

                # Move to next key point
                if self.next_key_point_ind < len(self.key_points) - 1:
                    self.current_key_point_ind = self.next_key_point_ind
                    self.next_key_point_ind += 1

                # If at end of path
                else:
                    self._reverse_path()
                    
                    self.current_key_point_ind = 0
                    self.next_key_point_ind = 1
                
                """
                # When next key tile reached, check if it has a door.
                if len(game_vars.room_list[self.current_room].tiles[self.current_tile].obj) > 0:
                    for o in game_vars.room_list[self.current_room].tiles[self.current_tile].obj:
                        if o.obj_type == Obj_Type.door:

                            # Go through door
                            game_vars.room_list[self.current_room].chars.remove(self)
                            self.current_room = o.new_room
                            game_vars.room_list[self.current_room].chars.append(self)

                            self.pos.x = game_vars.room_list[o.new_room].tiles[o.go_to].pos.x + TILE_W/2
                            self.pos.y = game_vars.room_list[o.new_room].tiles[o.go_to].pos.y - self.size.y/2

                # List of nearby tiles
                above_tile = self.current_tile - 1
                below_tile = self.current_tile + 1
                left_tile = self.current_tile - game_vars.room_list[self.current_room].rows
                right_tile = self.current_tile + game_vars.room_list[self.current_room].rows

                check_tiles = [above_tile, below_tile, left_tile, right_tile]

                # Check  for interaction
                for t in check_tiles:
                    if len(game_vars.room_list[self.current_room].tiles[t].obj) > 0:
                        for o in game_vars.room_list[self.current_room].tiles[t].obj:
                            if o.obj_type == Obj_Type.interact:
                                
                                # Kill character
                                if o.active == True:
                                    character.alive = False"""

            # If at next tile but not key point
            else:
                self.next_tile_ind += 1

        self._set_direction(game_vars, character)