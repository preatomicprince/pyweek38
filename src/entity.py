from pathlib import Path
import pygame
from settings import *
from spritesheet import SpriteSheet


class Ent:
    ent_count = 0

    def __init__(self, x_pos: float, y_pos: float, filepath: str, animation_steps: int = 1, ind: int = 0)  -> None:
        self.pos = fvec2(x_pos, y_pos)
        self.vel = fvec2(0, 0)
        self.dir: Direction = 0
        
        BLACK_GRE = (11, 158, 3)
        image = pygame.image.load(Path(filepath)).convert_alpha()
        
        self.size = ivec2(image.get_rect().w/animation_steps, image.get_rect().h)

        self.sprites = SpriteSheet(image, animation_steps, self.size.x, self.size.y, ind)
        
        Ent.ent_count += 1

    def draw(self, screen):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        screen.blit(self.sprites.animation_list[self.sprites.ind], rect)

    def get_bottom_pos(self) -> fvec2:
        return fvec2(self.pos.x + self.size.x/2, self.pos.y + self.size.y - 5)

