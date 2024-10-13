import pygame
from pygame.locals import *
from settings import Settings
import sys

def restart(settings):
    settings.running = False
    settings.restart = True

class Input:
    def __init__(self) -> None:
        self.key_left: bool = False
        self.key_right: bool = False
        self.key_up: bool = False
        self.key_down: bool = False
        self.key_interact: bool = False

        self.prev_input = None
        

    def update(self, buttons, settings: Settings, prev_input):

        _copy_input(prev_input, self)

        for event in pygame.event.get():
            if event.type == QUIT:
                settings.running = False
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    settings.running = False
                    sys.exit()

                if event.key == K_RIGHT or event.key == K_d:
                    self.key_right = True

                if event.key == K_LEFT or event.key == K_a:
                    self.key_left = True

                if event.key == K_UP or event.key == K_w:
                    self.key_up = True

                if event.key == K_DOWN or event.key == K_s:
                    self.key_down = True

                if event.key == K_e:
                    self.key_interact = True

                #if event.key == K_SPACE:
                    #restart(settings)


            if event.type == KEYUP:
                ###this controls the text at the begining of the level
                if settings.off_screen == False:
                    settings.off_screen = True

                if event.key == K_RIGHT or event.key == K_d:
                    self.key_right = False

                if event.key == K_LEFT or event.key == K_a:
                    self.key_left = False

                if event.key == K_UP or event.key == K_w:
                    self.key_up = False

                if event.key == K_DOWN or event.key == K_s:
                    self.key_down = False

                if event.key == K_e:
                    self.key_interact = False
            
            
            if event.type == MOUSEBUTTONDOWN:
            ####to feed in the button list
                pass

            if event.type == MOUSEBUTTONUP:
                for b in range(len(buttons)):
                    if buttons[b].over == True:
                        if buttons[b].name == "play":
                            settings.off_screen = True
  

def _copy_input(input1: Input, input2: Input):
    input1.key_left = input2.key_left
    input1.key_right = input2.key_right
    input1.key_up = input2.key_up
    input1.key_down = input2.key_down
    input1.key_interact = input2.key_interact

    input1.prev_input = None
