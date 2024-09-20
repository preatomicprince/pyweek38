from entity import Ent
from enum import Enum
from object import Obj, Obj_Type, Death_Type
from pathing import Path_Tile, Pathing
import pygame
from settings import SPEED, Direction, fvec2, TILE_W, TILE_H

Char = Enum("Char", ["heir", "duke", "duchess", "cleaner", "lady"])

class Character(Ent):
    def __init__(self, x_pos, y_pos, char: Char):
        self.char = char
        
        self.dir = None
        self.prev_dir = None
        
        self.death_type = None

        # Start frame for each direction's walk cycle
        # End frame should be the next start minus 1
        self.dl_start = 0
        self.dr_start = 8
        self.ur_start = 16
        self.ul_start = 24

        # Room the character is in
        self.current_room = 0
        self.walking_animation_steps = 32
        
        self.prev_alive = True
        self.alive = True

        match self.char:
            case Char.heir:
                self.animation_steps = 34
                self.current_room = 5

                self.key_points = [Path_Tile(5, 0), Path_Tile(5, 1, interaction = True), Path_Tile(5, 14, door = True),
                                   Path_Tile(1, 5), Path_Tile(1, 25, interaction = True, wait = 15)]
                self.path_tiles = [[0, 1], [1, 2, 14], [14, 5], [5, 25]]
                filepath = "../res/the_heir.png"

            case Char.duke:
                self.animation_steps = 39
                self.current_room = 3

                self.key_points = [Path_Tile(3, 5, interaction = True, wait = 15), Path_Tile(3, 11, door = True), Path_Tile(2, 12, door = True), Path_Tile(2, 10, interaction = True, wait = 5)]

                self.path_tiles = [[5, 6, 10, 11], [11, 12], [12, 13, 14, 15, 16, 10]]

                filepath = "../res/duke_sprite.png"

            case Char.duchess:
                self.current_room = 6
                self.walking_animation_steps = 4
                self.animation_steps = 9
                self.dr_start = 1
                self.ur_start = 2
                self.ul_start = 3

                self.key_points = [Path_Tile(6, 4, interaction = True, wait = 7),  Path_Tile(6, 8), Path_Tile(6, 11, door = True),
                                   Path_Tile(7, 6, door = True), Path_Tile(7, 7), Path_Tile(7, 13), Path_Tile(7, 12, interaction = True, wait = 5)]
                self.path_tiles = [[4, 8], [8, 9, 10, 11], [11, 6], [6, 7], [7, 13], [13, 12]]
                filepath = "../res/mother.png"

            case Char.cleaner:
                self.animation_steps = 37
                self.current_room = 7

                self.key_points = [Path_Tile(7, 13), Path_Tile(7, 1, interaction = True, wait = 5), Path_Tile(7, 7), Path_Tile(7, 6, door = True),
                                   Path_Tile(6, 11, door = True), Path_Tile(6, 16, door = True),
                                   Path_Tile(1, 6, door = True), Path_Tile(1, 0, interaction = True, wait = 5)]
                self.path_tiles = [[13, 1], [1, 7], [7, 6], [6, 11], [11, 8, 16], [16, 6], [6, 0]]
                filepath = "../res/the_maid.png"

            case Char.lady:
                self.current_room = 4
                self.walking_animation_steps = 16
                self.animation_steps = 21
                self.dr_start = 4
                self.ur_start = 8
                self.ul_start = 12

                self.key_points = [Path_Tile(4, 2, interaction = True, wait = 3), Path_Tile(4, 13, door = True), 
                                   Path_Tile(1, 1, door = True), Path_Tile(1, 1, interaction = True, wait = 1), Path_Tile(1, 3), Path_Tile(1, 33, door = True), 
                                   Path_Tile(3, 3, door = True), Path_Tile(3, 11, door = True),
                                   Path_Tile(2, 12, door = True), Path_Tile(2, 15)]
                self.path_tiles = [[2, 14, 13], [13, 1], [1,1], [1, 3], [3, 33], [33, 3], [3, 11], [11, 12], [12, 15]]
                filepath = "../res/grandma.png"

        self.pathing = Pathing(self.key_points, self.path_tiles, self.current_room)

        super().__init__(x_pos, y_pos, filepath, self.animation_steps)

        self.pos.x = x_pos + TILE_W/2 - self.size.x/2
        self.pos.y = y_pos + TILE_H/2 - self.size.y + 20

    def update(self, game_vars) -> None:

        if self.alive == False:
            if self.prev_alive == True:
                self.prev_alive = False
                game_vars.score += 250000
                print("DEAD")
                self._set_death_animation()
        else:
            self.pathing.update(game_vars, self)

            if self.pathing.timer == None:
                self.pos.x += self.vel.x
                self.pos.y += self.vel.y

        self.sprites.update(game_vars.time)


    def draw(self, screen):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        
        if self.alive:
            screen.blit(self.sprites.animation_list[self.sprites.ind], rect)
            return
        else:
            angle = 180
            rect = pygame.Rect(self.pos.x, self.pos.y + self.size.y/2, self.size.x, self.size.y)
            rotated_image = pygame.transform.rotate(self.sprites.animation_list[self.sprites.ind], angle)

            screen.blit(rotated_image, rect)

    def _set_death_animation(self):

        match self.death_type:
            case Death_Type.explode:
                if self.char == Char.duke:
                    self.sprites.set_animation(32, 32, repeat = False)

                if self.char == Char.lady:
                    self.sprites.set_animation(19, 20, repeat = False)

            case Death_Type.poison:
                if self.char == Char.duke:
                    self.sprites.set_animation(33, self.animation_steps - 1, repeat = False)

                if self.char == Char.duchess:
                    self.sprites.set_animation(4, self.animation_steps - 1, repeat = False)

            case Death_Type.electrecute:
                if self.char == Char.lady:
                    self.sprites.set_animation(16, 17, repeat = 10)

                if self.char == Char.heir:
                    self.sprites.set_animation(32, 33, repeat = 10)

            case Death_Type.chop:
                if self.char == Char.lady:
                    self.sprites.set_animation(19, 20, repeat = False)

                if self.char == Char.cleaner:
                    self.sprites.set_animation(35, 36, repeat = False)
        
            case Death_Type.crush:
                if self.char == Char.duchess:
                    self.sprites.set_animation(4, self.animation_steps - 1, repeat = False)


            case Death_Type.fall:
                if self.char == Char.heir:
                    pass

                if self.char == Char.cleaner:
                    pass

 
