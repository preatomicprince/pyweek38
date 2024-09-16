from entity import Ent
from object import Obj
import pygame
from settings import TILE_H

class Tile(Ent):
    def __init__(self, x_pos: float, y_pos: float, obj: Obj = None, ind: int = 0):
        filepath = "../res/tile1.png"
        animation_steps = 2
        self.obj = []
        
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)

    def draw_obj(self, screen, ind: int):
            y_pos = self.pos.y - self.obj[ind].size.y + TILE_H
            rect = pygame.Rect(self.pos.x, y_pos, self.obj[ind].size.x, self.obj[ind].size.y)

            screen.blit(self.obj[ind].sprites.animation_list[self.obj[ind].sprites.ind], rect)

