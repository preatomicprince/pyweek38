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

    def draw_obj(self, screen):
        for o in self.obj:
            y_pos = self.pos.y - o.size.y + TILE_H
            rect = pygame.Rect(self.pos.x, y_pos, o.size.x, o.size.y)

            screen.blit(o.sprites.animation_list[o.sprites.ind], rect)

