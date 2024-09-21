from object import Obj_Type, Interact_Type, Death_Type
from text import Text
from typedefs import fvec2, Direction, SPEED, TILE_W, TILE_H


class Path_Tile:
    def __init__(self, room: int, tile: int,
                 door: bool = False, interaction: bool = False, wait: int = 0, text: str = None) -> None:
        
        #index of room in room_list[]
        self.room = room
        #index of tile in room.tiles[]
        self.tile = tile
        
        # If True, check for door on tile and walk through
        self.door = door

        # If true, interact with object on adjacent tile
        self.interaction = interaction      

        # Time in seconds to wait before starting to move to next key point
        self.wait = wait*1000 

        self.text = text


class Pathing:
    def __init__(self, key_points = None, path_tiles = None, current_room = 0) -> None:

        # All major stops and key interaction tiles
        # List of Path_Tiles
        self.key_points: list = key_points

        # All stops between key points
        # List of tile indexes (int)
        # Should contain (len(self.key_points) - 1) lists
        # First in each list should be current key point. Last should be next key point
        self.path_tiles =  path_tiles

        # Index for room_list
        self.current_room = current_room

        self.current_tile = self.path_tiles[0][0]
        
        # Indexes in self.path_list
        self.next_tile_ind = 1

        # Indexes in self.key_points
        self.current_key_point_ind = 0
        self.next_key_point_ind = 1

        self.timer = None


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
        
        """
        if char_tile_coord == None:
            character.pos.x = game_vars.room_list[self.current_room].tiles[self.key_points[self.current_key_point_ind].tile].pos.x + TILE_W/2 - self.size.x/2
            character.pos.y = game_vars.room_list[self.current_room].tiles[self.key_points[self.current_key_point_ind].tile].pos.y + TILE_H/2 - self.size.y + 20
            self.current_tile = game_vars.room_list[self.current_room].find_ent_tile(character)
            char_tile_coord = game_vars.room_list[self.current_room].ind_to_coord(self.current_tile) 
        """


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

    def _handle_interaction(self, game_vars, character) -> None:
        # Checks for interaction with nearby character and kills them

        if self.key_points[self.next_key_point_ind].interaction == True:
            
            next_key_point = self.key_points[self.next_key_point_ind].tile

            # List of nearby tiles
            above_tile = next_key_point - 1
            below_tile = next_key_point + 1
            left_tile = next_key_point - game_vars.room_list[self.current_room].rows
            right_tile = next_key_point + game_vars.room_list[self.current_room].rows

            check_tiles = [next_key_point, above_tile, below_tile, left_tile, right_tile]

            # Check  for interaction
            for t in check_tiles:
                cols = game_vars.room_list[self.current_room].cols
                rows = game_vars.room_list[self.current_room].rows

                if t not in range(rows*cols):
                    continue

                if len(game_vars.room_list[self.current_room].tiles[t].obj) == 0:
                    
                    continue

                for o in game_vars.room_list[self.current_room].tiles[t].obj:
                    if o.obj_type == Obj_Type.interact and o.active:

                        # Kill character
                        character.alive = False
                        
                        match o.interact_type:
                            case Interact_Type.stove:
                                character.death_type = Death_Type.explode

                            case Interact_Type.whiskey:
                                character.death_type = Death_Type.poison

                            case Interact_Type.wine:
                                character.death_type = Death_Type.poison

                            case Interact_Type.gramophone:
                                character.death_type = o.death_type

                            case Interact_Type.armour:
                                o.active = False
                                character.death_type = Death_Type.chop

                            case Interact_Type.telephone:
                                character.death_type = Death_Type.electrecute

                            case Interact_Type.bookshelf:
                                character.death_type = Death_Type.crush

    def _handle_doors(self, game_vars, character) -> None:
        # When next key tile reached, check if it has a door.
        if self.key_points[self.next_key_point_ind].door == True:
            if self.key_points[self.next_key_point_ind].room != self.key_points[self.next_key_point_ind + 1].room:
                
                for o in game_vars.room_list[self.current_room].tiles[self.current_tile].obj:
                    if o.obj_type == Obj_Type.door:
                        # Go through door
                        game_vars.room_list[self.current_room].chars.remove(character)
                        self.current_room = o.new_room
                        character.current_room = o.new_room
                        game_vars.room_list[self.current_room].chars.append(character)

                        character.pos.x = game_vars.room_list[o.new_room].tiles[o.go_to].pos.x + TILE_W/2 - character.size.x/2
                        character.pos.y = game_vars.room_list[o.new_room].tiles[o.go_to].pos.y + 20 + TILE_H/2 - character.size.y
    
   
    def update(self, game_vars, character) -> None:
        self.current_tile = game_vars.room_list[self.current_room].find_ent_tile(character)
        
                
                

        next_tile = self.path_tiles[self.current_key_point_ind][self.next_tile_ind]

        
        next_key_point = self.key_points[self.next_key_point_ind].tile
        if self.current_tile == next_tile:
            if self.current_tile != next_key_point:
                self.next_tile_ind += 1

            # If reached key point
            elif self.current_tile == next_key_point:

               
                if self.key_points[self.next_key_point_ind].wait > 0:
                    if self.timer == None:
                         # Add text event
                        if self.key_points[self.next_key_point_ind].text != None:
                            game_vars.text_events.append(game_vars, self.key_points[self.next_key_point_ind].text)
                            character.text = Text(game_vars.time, self.key_points[self.next_key_point_ind].text, self.key_points[self.next_key_point_ind].wait)

                        self._handle_interaction(game_vars, character)
                        self.timer = game_vars.time
                    else:
                        if game_vars.time > self.timer + self.key_points[self.next_key_point_ind].wait:
                            self.timer = None

                if self.timer == None:
                    self._handle_interaction(game_vars, character)
                    self._handle_doors(game_vars, character)
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
            

            elif self.current_room == 3 :
                print(self.current_tile)

                for i in self.path_tiles[self.current_key_point_ind]:
                    on_path = False
                    if self.current_tile != i:
                        continue
                    on_path = True
                    
                    break
                
                if on_path == False:
                    current_key_tile = self.key_points[self.current_key_point_ind].tile

                    
                    print(f"current key tile: {current_key_tile}")

                    key_tile_pos = game_vars.room_list[self.current_room].tiles[current_key_tile].pos
                    nt_pos = game_vars.room_list[self.current_room].tiles[self.path_tiles[self.current_key_point_ind][self.next_tile_ind+1]].pos
                    print(f"x{key_tile_pos.x}")
                    self.next_tile_ind = 1
                    character.pos.x = nt_pos.x+ TILE_W/2 - character.size.x/2
                    character.pos.y = nt_pos.y + 20 + TILE_H/2 - character.size.y

        self.current_tile = game_vars.room_list[self.current_room].find_ent_tile(character)
        self._set_direction(game_vars, character)