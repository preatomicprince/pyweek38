import pygame
from pathlib import Path

base_fps = 10

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

        self.start_frame = 0
        self.end_frame = animation_steps - 1
        self.fps = base_fps

        self.prev_frame_time = 0

        self.repeat = True
        
        ###the colour used in the background of sprites that gets cut out to make it transparent
        ##the bit you want to cut out has to be this colour
        BLACK_GRE = (11, 158, 3)
        
        for x in range(self.animation_steps):
            self.animation_list.append(self._get_image(x, self.x_cut, self.y_cut, BLACK_GRE))
            
            
    def _get_image(self, frame, width, height, colour):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((frame * width), 0 , width, height))
        image.set_colorkey(colour)
        return image

    def set_animation(self, start_frame, end_frame, fps = base_fps, repeat: bool = True) -> None:
        # Sets the start and end frames for certain parts of the sprite sheet
        # Used for calling specific animations from different parts of the same sheet

        self.start_frame = start_frame
        self.end_frame = end_frame
        self.fps = fps
        
        self.ind = self.start_frame

        self.repeat = repeat

    def update(self, time) -> None:
        # Moves animation to next frame if enough time has passed

        if time > self.prev_frame_time + 1000/self.fps:
            self.prev_frame_time = time
            if self.ind < self.end_frame:
                self.ind += 1
            elif self.repeat == True:
                self.ind = self.start_frame

        