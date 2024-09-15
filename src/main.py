import pygame
from pygame.locals import *
import sys

RUNNING = True
WIDTH = 500
HEIGHT = 300

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    while RUNNING:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                RUNNING = False
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    RUNNING = False
                    sys.exit()

        pygame.display.update()