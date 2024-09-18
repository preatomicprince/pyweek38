from settings import GameVars, ivec2, Direction
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
    def __init__(self, key_points, path_tiles) -> None:

        # All major stops and key interaction tiles
        # List of Path_Tiles
        self.key_points: list = [Path_Tile(3, 0), Path_Tile(3, 3, door = True), Path_Tile(0, 0), Path_Tile(0, 3)]

        # All stops between key points
        # List of tile indexes (int)
        # Should contain (len(self.key_points) - 1) lists
        # First in each list should be current key point. Last should be next key point
        self.path_tiles: list = [[0, 1, 2, 3], [3, 0], [3, 2, 1, 0]]

        # Index for room_list
        self.current_room = 0
        self.current_tile = self.path_tiles[0][0]
        
        # Indexes in self.path_list
        self.next_tile_ind = 1

        # Indexes in self.key_points
        self.current_key_point_ind = 0
        self.next_key_point_ind = 1

    def _reverse_path(self) -> None:
        # Reverses path so character traverses back to start

        self.key_points.reverse()

        for i in self.next_tile:
            i.reverse()

        self.next_tile.reverse()

    def _set_direction(self, game_vars, character):
        char_tile_coord = game_vars.room_list[self.current_room].ind_to_coord(self.current_tile)

        next_tile = self.path_tiles[self.current_key_point_ind][self.next_tile_ind]
        next_tile_coord = game_vars.room_list[self.current_room].ind_to_coord(next_tile)

        if next_tile_coord.x > char_tile_coord.x:
            character.dir = Direction.dr
        elif next_tile_coord.x < char_tile_coord.x:
            character.dir = Direction.ul
        elif next_tile_coord.y > char_tile_coord.y:
            character.dir = Direction.dl
        elif next_tile_coord.y < char_tile_coord.y: 
            character.dir = Direction.ur

    def update(self, game_vars, character):
        self.current_tile = game_vars.room_list.get_ent_tile(character)

        next_tile = self.path_tiles[self.current_key_point_ind][self.next_tile_ind]
        next_key_point = self.key_points[self.next_key_point_ind].tile

        if self.current_tile == next_tile:
            if self.current_tile == next_key_point:
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

            # If at next tile but not key point
            else:
                self.next_tile += 1