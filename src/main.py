from entity import Ent
from input import Input
from object import Obj
from player import Player
import pygame
from room import Room
from settings import Settings, WIDTH, HEIGHT

if __name__ == "__main__":
    pygame.init()
    settings = Settings()
    input = Input()
    prev_input = Input()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    player = Player(200, 200)

    new_room = Room(5, 5)

    new_room.tiles[0].obj = Obj("./res/box1.png")

    while settings.running:
        screen.fill((128, 128, 128))

        input.update(settings, prev_input)
        player.update(input)
        
        new_room.draw(screen)
        player.draw(screen)
        pygame.display.update()