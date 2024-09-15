import pygame
from pygame.locals import *
from settings import Settings
import sys

class Input:
    def __init__(self) -> None:
        self.key_left: bool = False
        self.key_right: bool = False
        self.key_up: bool = False
        self.key_down: bool = False
        self.interact: bool = False

    def update(self, settings: Settings, prev_input):

        _copy_input(prev_input, self)

        for event in pygame.event.get():
            if event.type == QUIT:
                settings.running = False
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    settings.running = False
                    sys.exit()

                if event.key == K_RIGHT:
                    self.key_right = True

                if event.key == K_LEFT:
                    self.key_left = True

                if event.key == K_UP:
                    self.key_up = True

                if event.key == K_DOWN:
                    self.key_down = True


            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.key_right = False

                if event.key == K_LEFT:
                    self.key_left = False

                if event.key == K_UP:
                    self.key_up = False

                if event.key == K_DOWN:
                    self.key_down = False

  

def _copy_input(input1: Input, input2: Input):
    input1.key_left = input2.key_left
    input1.key_right = input2.key_right
    input1.key_up = input2.key_up
    input1.key_down = input2.key_down
    input1.interact = input2.interact

    input1.prev_input = None
