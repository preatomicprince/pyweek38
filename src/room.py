from entity import Ent
from object import Obj, Obj_Type
from player import Player
from tile import Tile
from typedefs import Direction, TILE_W, TILE_H, WIDTH, ivec2



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
                    ind = 0
                else:
                    ind = 1
                self.tiles.append(Tile(((x - y)*(TILE_W/2) + WIDTH/2 + ((self.rows - self.cols)*TILE_W/2/2) - TILE_W/2), ((x + y)*(TILE_H/2) + TILE_H*4), ind=ind))

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
                    if  tile.obj[i].obj_type == Obj_Type.decor or tile.obj[i].obj_type == Obj_Type.other:
                        if tile.pos.y + TILE_H/2 < player.pos.y + player.size.y:
                            tile.draw_obj(screen, i)

        for tile in self.tiles:
            if len(tile.obj) > 0:
                for i in range(len(tile.obj)):
                    if tile.obj[i].obj_type == Obj_Type.door or tile.obj[i].obj_type == Obj_Type.interact or tile.obj[i].obj_type == Obj_Type.pickup:
                        tile.draw_obj(screen, i)

        

        for character in self.chars:
            if character.pos.y < player.pos.y:
                character.draw(screen)

        player.draw(screen) # can be adjusted to work for all characters

        for character in self.chars:
            if character.pos.y > player.pos.y:
                character.draw(screen)

        for tile in self.tiles:
            if len(tile.obj) > 0:
                for i in range(len(tile.obj)):
                    if tile.obj[i].obj_type == Obj_Type.decor or tile.obj[i].obj_type == Obj_Type.other:
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

    def set_interact(self, game_vars, player: Player) -> None:

        ###need to put bark in here
        ###for the objects

        # Checks if interactable object is on current tile or tile player is facing.
        # Selects object so player will interact when e key is pressed

        pti = self.find_ent_tile(player)
        if pti != None:
            
            # Check and set interactable obj on player's current tile        
            if self.tiles[pti].obj != None:
                for o in self.tiles[pti].obj:
                    if o.interact == True:
                        if player.selected_obj != None:
                            player.selected_obj.selected = False
                            player.selected_obj.sprites.ind -= 1
                        player.selected_obj = o
                        o.selected = True
                        player.selected_obj.sprites.ind += 1
                        return
                    
            pt = self.ind_to_coord(pti)

            # Set checking tile to one next to player, in direction they're facing
            match player.dir:
                case Direction.dr:
                    pt.x += 1

                case Direction.ul:
                    pt.x -= 1
                    
                case Direction.ur:
                    pt.y -= 1

                case Direction.dl:
                    pt.y += 1

            # Check new tile for interactable object and set it
            if 0 <= pt.x < self.cols and 0 <= pt.y < self.rows:
                pti = self.coord_to_ind(pt.x, pt.y)
                if len(self.tiles[pti].obj) > 0:
                    for o in self.tiles[pti].obj:
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
                




