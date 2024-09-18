from entity import Ent
from object import Obj, Obj_Type
from player import Player
from settings import Direction, TILE_W, TILE_H, WIDTH, HEIGHT, fvec2, ivec2
from tile import Tile



class Room:
    def __init__(self, room_name, rows, cols) -> None:
        #if we compare the room name to the current room in the game vars, we can show specific rooms
        self.room_name = room_name
        
        self.rows = rows
        self.cols = cols
        self.tiles: list = []

        self.chars = []

        for x in range(cols):
            for y in range(rows):
                #https://clintbellanger.net/articles/isometric_math/ idk
                ##makes the distincation between the rooms for different floor tiles
                if self.room_name == "kitchen":
                    self.tiles.append(Tile(((x - y)*(TILE_W/2) + WIDTH/2), ((x + y)*(TILE_H/2) + HEIGHT/2), ind=0) )
                else:
                    self.tiles.append(Tile(((x - y)*(TILE_W/2) + WIDTH/2), ((x + y)*(TILE_H/2) + HEIGHT/2), ind=1) )

    def coord_to_ind(self, x: int, y: int) -> int:
        return x*self.rows + y
    
    def ind_to_coord(self, ind: int) -> ivec2:
        for c in range(1, self.cols + 1):
            if c*self.rows <= ind:
                continue
            else:
                return ivec2(c - 1, ind - (c-1)*self.rows)

    def draw(self, screen, player):
        for tile in self.tiles:
            tile.draw(screen)

        for tile in self.tiles:
            if len(tile.obj) > 0:
                for i in range(len(tile.obj)):
                    if tile.obj[i].obj_type == Obj_Type.wall:
                        tile.draw_obj(screen, i)

        for tile in self.tiles:
            if len(tile.obj) > 0:
                for i in range(len(tile.obj)):
                    if tile.obj[i].obj_type == Obj_Type.door:
                        tile.draw_obj(screen, i)

        for tile in self.tiles:
            if len(tile.obj) > 0:
                for i in range(len(tile.obj)):
                    if tile.obj[i].obj_type != Obj_Type.wall and tile.obj[i].obj_type != Obj_Type.door:
                        if tile.pos.y + TILE_H/2 < player.pos.y + player.size.y:
                            tile.draw_obj(screen, i)

        player.draw(screen) # can be adjusted to work for all characters
        for character in self.chars:
            character.draw(screen)

        for tile in self.tiles:
            if len(tile.obj) > 0:
                for i in range(len(tile.obj)):
                    if tile.obj[i].obj_type != Obj_Type.wall and tile.obj[i].obj_type != Obj_Type.door:
                        if tile.pos.y + TILE_H/2 > player.pos.y + player.size.y:
                            tile.draw_obj(screen, i)

    def add_walls(self, filepath: str):
        for c in range(self.cols):
            for r in range(self.rows):
                if c == 0:
                    self.tiles[self.coord_to_ind(c, r)].obj.append(Obj(filepath, ind=0, obj_type = Obj_Type.wall)) 
                if r == 0:
                    self.tiles[self.coord_to_ind(c, r)].obj.append(Obj(filepath, ind=1, obj_type = Obj_Type.wall)) 

    def find_ent_tile(self, ent: Ent) -> int:
        # Returns tile index ent is standing in
        bottom_pos = ent.get_bottom_pos()

        for x in range(self.cols):
            for y in range(self.rows):
                if (bottom_pos.x > self.tiles[self.coord_to_ind(x, y)].pos.x) and (bottom_pos.x < self.tiles[self.coord_to_ind(x, y)].pos.x + TILE_W):
                    if (bottom_pos.y > self.tiles[self.coord_to_ind(x, y)].pos.y) and (bottom_pos.y < self.tiles[self.coord_to_ind(x, y)].pos.y + TILE_H):
                        return self.coord_to_ind(x, y)

    def set_interact(self, player: Player) -> None:
        # Checks if interactable object is on current tile or tile player is facing.
        # Selects object so player will interact when e key is pressed

        p_tile = self.find_ent_tile(player)
        if p_tile != None:
            
        # Check and set interactable obj on player's current tile        
            if self.tiles[p_tile].obj != None:
                for o in self.tiles[p_tile].obj:
                    if o.interact == True:
                        if player.selected_obj != None:
                            player.selected_obj.selected = False
                            player.selected_obj.sprites.ind -= 1
                        player.selected_obj = o
                        o.selected = True
                        player.selected_obj.sprites.ind += 1
                        return

            # Set checking tile to one next to player, in direction they're facing
            match player.dir:
                case Direction.dr:
                    p_tile += self.rows

                case Direction.ul:
                    p_tile -= self.rows
                    
                case Direction.ur:
                    p_tile -= 1

                case Direction.dl:
                    p_tile += 1

            # Check new tile for interactable object and set it
            if 0 < p_tile < len(self.tiles):
                if self.tiles[p_tile].obj != None:
                    for o in self.tiles[p_tile].obj:
                        if o.interact == True:
                            if player.selected_obj != None:
                                player.selected_obj.selected = False
                                player.selected_obj.sprites.ind -= 1
                            player.selected_obj = o
                            o.selected = True
                            player.selected_obj.sprites.ind += 1
                            return

        if player.selected_obj != None:
            player.selected_obj.selected = False
            player.selected_obj.sprites.ind -= 1
            player.selected_obj = None
                




