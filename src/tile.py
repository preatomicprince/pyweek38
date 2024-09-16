from entity import Ent
from object import Obj, Obj_Type
import pygame
from settings import TILE_W, TILE_H

class Tile(Ent):
    def __init__(self, x_pos: float, y_pos: float, obj: Obj = None, ind: int = 0):
        filepath = "../res/kitchen_tiles2.png"
        animation_steps = 1
        self.obj = []
        
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)

    def draw_obj(self, screen, ind: int):
            if self.obj[ind].obj_type == Obj_Type.pickup:
                y_pos = self.pos.y + TILE_H/2 - self.obj[ind].size.y
                x_pos = self.pos.x + TILE_W/2 - self.obj[ind].size.x/2
                rect = pygame.Rect(x_pos, y_pos, self.obj[ind].size.x, self.obj[ind].size.y)
            else:
                y_pos = self.pos.y - self.obj[ind].size.y + TILE_H
                rect = pygame.Rect(self.pos.x, y_pos, self.obj[ind].size.x, self.obj[ind].size.y)

            screen.blit(self.obj[ind].sprites.animation_list[self.obj[ind].sprites.ind], rect)

