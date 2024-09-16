from object import Obj
from player import Player
from settings import TILE_W, TILE_H, WIDTH, HEIGHT
from tile import Tile

class Room:
    def __init__(self, room_name, rows, cols) -> None:
        #if we compare the room name to the current room in the game vars, we can show specific rooms
        self.room_name = room_name
        
        self.rows = rows
        self.cols = cols
        self.tiles: list = []

        ##not permenant, im just putting this in to test how it looks
        wall_file = "../res/tile1.png"
        self.wall_list: list = []

        for x in range(cols):
            for y in range(rows):
                #https://clintbellanger.net/articles/isometric_math/ idk
                ##makes the distincation between the rooms for different floor tiles
                if self.room_name == "kitchen":
                    self.tiles.append(Tile(((x - y)*(TILE_W/2) + WIDTH/2), ((x + y)*(TILE_H/2) + HEIGHT/2), ind=0) )
                else:
                    self.tiles.append(Tile(((x - y)*(TILE_W/2) + WIDTH/2), ((x + y)*(TILE_H/2) + HEIGHT/2), ind=1) )

    def draw(self, screen, player):
        for tile in self.tiles:
            tile.draw(screen)

        for tile in self.tiles:
            if tile.obj != None:
                if tile.pos.y + TILE_H/2 < player.pos.y + player.size.y:
                    tile.draw_obj(screen)

        player.draw(screen) # can be adjusted to work for all characters

        for tile in self.tiles:
            if tile.obj != None:
                if tile.pos.y + TILE_H/2 > player.pos.y + player.size.y:
                    tile.draw_obj(screen)

    def add_walls(self, filepath: str):
        for c in range(self.cols):
            for r in range(self.rows):
                if c == 0:
                    self.tiles[c*self.rows + r].obj.append(Obj(filepath, animation_steps=2, ind=0)) 
                if r == 0:
                    self.tiles[c*self.rows + r].obj.append(Obj(filepath, animation_steps=2, ind=1))    