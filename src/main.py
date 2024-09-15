from entity import Ent
from input import Input
from player import Player
import pygame
from settings import Settings, WIDTH, HEIGHT

if __name__ == "__main__":
    pygame.init()
    settings = Settings()
    input = Input()
    prev_input = Input()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    player = Player(200, 200)

    while settings.running:
        screen.fill((128, 128, 128))

        input.update(settings, prev_input)
        player.update(input)
        
        player.draw(screen)
        pygame.display.update()