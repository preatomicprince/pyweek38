from player import Player
from settings import TILE_W, TILE_H, WIDTH, HEIGHT
from tile import Tile

class Room:
    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = rows
        self.tiles: list = []

        for x in range(cols):
            for y in range(rows):
                #https://clintbellanger.net/articles/isometric_math/ idk
                self.tiles.append(Tile(((x - y)*(TILE_W/2) + WIDTH/2), ((x + y)*(TILE_H/2) + HEIGHT/2)))

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