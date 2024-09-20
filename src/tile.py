from entity import Ent
from object import Obj, Obj_Type
from pathlib import Path
import pygame
from settings import TILE_W, TILE_H, ivec2
from spritesheet import SpriteSheet

class Tile(Ent):
    def __init__(self, x_pos: float, y_pos: float, obj: Obj = None, ind: int = 0):
        filepath = "../res/tile1.png"
        animation_steps = 2
        self.obj = []

        exclamation = pygame.image.load(Path("../res/ui.png")).convert_alpha()
        exclamation_size = ivec2(exclamation.get_rect().w/9, exclamation.get_rect().h)
        self.exclamation = SpriteSheet(exclamation, 9, exclamation_size.x, exclamation_size.y, ind = 2)
        
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)

    def draw_obj(self, screen, ind: int):
            
            # draw pickup in centr, not offset
            if self.obj[ind].obj_type == Obj_Type.pickup:
                y_pos = self.pos.y + TILE_H/2 - self.obj[ind].size.y
                x_pos = self.pos.x + TILE_W/2 - self.obj[ind].size.x/2
                rect = pygame.Rect(x_pos, y_pos, self.obj[ind].size.x, self.obj[ind].size.y)
            else:
                y_pos = self.pos.y - self.obj[ind].size.y + TILE_H
                rect = pygame.Rect(self.pos.x, y_pos, self.obj[ind].size.x, self.obj[ind].size.y)
            
            screen.blit(self.obj[ind].sprites.animation_list[self.obj[ind].sprites.ind], rect)

            # Draw door exclamation
            if self.obj[ind].obj_type == Obj_Type.door:
                if self.obj[ind].danger:
                    if self.obj[ind].sprites.ind <= 1:
                         x_offset = 0
                    else:
                         x_offset = TILE_W/2
                    exrect = pygame.Rect(self.pos.x - 16 + x_offset, self.pos.y - self.exclamation.y_cut - 40, self.exclamation.x_cut, self.exclamation.y_cut)
                    screen.blit(self.exclamation.animation_list[self.exclamation.ind], exrect)
                    self.obj[ind].danger = False
