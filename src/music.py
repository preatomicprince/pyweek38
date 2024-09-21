import pygame
from pathlib import Path



class Music_Sound:
    def __init__(self, tag, file_loc, vol = 1):
        self.tag = tag
        self.file_loc = file_loc
        self.vol = vol

    def play(self):
        name = pygame.mixer.Sound(self.file_loc)

        ###zero tag means this track will play on loop
        if self.tag == 0:
            name.play(-1)
        ###thisll play once
        if self.tag == 1:
            name.play()

    def load(self):
        ###to load the track before playing it
        pygame.mixer.music.load(self.file_loc)
        pygame.mixer.music.set_volume(self.vol)

#track.play()
#track = Music_Sound("./res/Dark Matter Long.wav") ##an example of how this will work 
#track.Load() this is to load what ever track has been made
#load the track then play it