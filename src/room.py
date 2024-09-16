from object import Obj, Obj_Type
from player import Player
from settings import Direction, TILE_W, TILE_H, WIDTH, HEIGHT, fvec2
from tile import Tile



class Room:
    def __init__(self, room_name, rows, cols) -> None:
        #if we compare the room name to the current room in the game vars, we can show specific rooms
        self.room_name = room_name
        
        self.rows = rows
        self.cols = cols
        self.tiles: list = []

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

    def find_player_tile(self, player: Player) -> int:
        # Returns tile index player is standing in
        p_bottom_pos = player.get_bottom_pos()

        for x in range(self.cols):
            for y in range(self.rows):
                if (p_bottom_pos.x > self.tiles[self.coord_to_ind(x, y)].pos.x) and (p_bottom_pos.x < self.tiles[self.coord_to_ind(x, y)].pos.x + TILE_W):
                    if (p_bottom_pos.y > self.tiles[self.coord_to_ind(x, y)].pos.y) and (p_bottom_pos.y < self.tiles[self.coord_to_ind(x, y)].pos.y + TILE_H):
                        return self.coord_to_ind(x, y)

    def set_interact(self, player: Player) -> None:
        p_tile = self.find_player_tile(player)
        if p_tile == None:
            return
        
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

        match player.dir:
            case Direction.dr:
                p_tile += self.rows

            case Direction.ul:
                p_tile -= self.rows
                
            case Direction.ur:
                p_tile -= 1

            case Direction.dl:
                p_tile += 1

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
                




