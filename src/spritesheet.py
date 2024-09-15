import pygame
from pathlib import Path

class SpriteSheet:
    def __init__(self, image, animation_steps, x_cut, y_cut, ind = 0):
        self.sheet = image
        self.animation_list = []
        self.animation_steps = animation_steps
        
        ###ind is used to define what image in the animation_list is used
        self.ind = ind
        
        ###this defines the size of the smaller sub image to be cut out of the picture
        self.x_cut = x_cut
        self.y_cut = y_cut
        
        ###the colour used in the background of sprites that gets cut out to make it transparent
        BLACK_GRE = (11, 158, 3)
        
        for x in range(self.animation_steps):
            self.animation_list.append(self.get_image(x, self.x_cut, self.y_cut, BLACK_GRE))
            
            
    def get_image(self, frame, width, height, colour):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((frame * width), 0 , width, height))
        image.set_colorkey(colour)
        return image
        