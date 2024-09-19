from pathlib import Path
import pygame
from spritesheet import *

class Buttons:
    def __init__(self, x, y, ind, name) -> None:
        self.x  = x
        self.y = y
        self.ind = ind
        self.name = name

        self.image = pygame.image.load(Path("../res/ui.png")).convert_alpha()

        self.rect = pygame.Rect(self.x, self.y, 120, 64)
        
        self.sprites = SpriteSheet(self.image, 8, 120, 64)

        ###to handle the interactions
        self.over = False

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.over = True
            screen.blit(self.sprites.animation_list[self.ind+1], self.rect)
        else:
            self.over = False
            screen.blit(self.sprites.animation_list[self.ind], self.rect)