from entity import Ent
from enum import Enum
from object import Obj, Obj_Type, Death_Type
from pathing import Path_Tile, Pathing
from pathlib import Path
import pygame
from spritesheet import SpriteSheet
from text import Text
from typedefs import ivec2, TILE_W, TILE_H
from music import Music_Sound

Char = Enum("Char", ["heir", "duke", "duchess", "cleaner", "lady"])

class Character(Ent):
    def __init__(self, x_pos, y_pos, char: Char):
        self.char = char
        
        self.dir = None
        self.prev_dir = None

        self.can_see_player = False

        exclamation = pygame.image.load(Path("../res/ui.png")).convert_alpha()
        exclamation_size = ivec2(exclamation.get_rect().w/9, exclamation.get_rect().h)
        self.exclamation = SpriteSheet(exclamation, 9, exclamation_size.x, exclamation_size.y, ind = 2)
        
        self.heading_to_door = False
        
        self.death_type = None

        self.text = None
        
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

                self.key_points = [Path_Tile(5, 0), Path_Tile(5, 1, interaction = True, wait =2, text = "The Heir is walking past the window in his bedroom"), Path_Tile(5, 14, door = True),
                                   Path_Tile(1, 5, door = True), Path_Tile(1, 25, interaction = True, wait = 15, text = "The Heir is making a phonecall")]
                self.path_tiles = [[0, 1], [1, 2, 14], [14, 5], [5, 25]]
                filepath = "../res/the_heir.png"

            case Char.duke:
                self.animation_steps = 39
                self.current_room = 3

                self.key_points = [Path_Tile(3, 5, interaction = True, wait = 15, text = "The Duke is smoking a cigarette in the kitchen"), Path_Tile(3, 11, door = True), Path_Tile(2, 12, door = True), Path_Tile(2, 10, interaction = True, wait = 5, text = "The Duke is drinking his whiskey in the dining room")]

                self.path_tiles = [[5, 6, 10, 11], [11, 12], [12, 13, 14, 15, 16, 10]]

                filepath = "../res/duke_sprite.png"

            case Char.duchess:
                self.current_room = 6
                self.walking_animation_steps = 4
                self.animation_steps = 9
                self.dr_start = 1
                self.ur_start = 2
                self.ul_start = 3

                self.key_points = [Path_Tile(6, 4, interaction = True, wait = 7, text = "The Duchess is drinking wine in the living room"),  Path_Tile(6, 8), Path_Tile(6, 11, door = True),
                                   Path_Tile(7, 6, door = True), Path_Tile(7, 7), Path_Tile(7, 13), Path_Tile(7, 12, interaction = True, wait = 5, text = "The duchess is picking a book to read in the library")]
                self.path_tiles = [[4, 8], [8, 9, 10, 11], [11, 6], [6, 7], [7, 13], [13, 12]]
                filepath = "../res/mother.png"

            case Char.cleaner:
                self.animation_steps = 37
                self.current_room = 7

                self.key_points = [Path_Tile(7, 13), Path_Tile(7, 1, interaction = True, wait = 5, text = "The Cleaner is cleaning a window in the library"), Path_Tile(7, 7), Path_Tile(7, 6, door = True),
                                   Path_Tile(6, 11, door = True), Path_Tile(6, 16, door = True),
                                   Path_Tile(1, 6, door = True), Path_Tile(1, 0, interaction = True, wait = 5, text = "The Cleaner is polishing the suit of armour in the hallway")]
                self.path_tiles = [[13, 1], [1, 7], [7, 6], [6, 11], [11, 8, 16], [16, 6], [6, 0]]
                filepath = "../res/the_maid.png"

            case Char.lady:
                self.current_room = 4
                self.walking_animation_steps = 16
                self.animation_steps = 21
                self.dr_start = 4
                self.ur_start = 8
                self.ul_start = 12

                self.key_points = [Path_Tile(4, 2, interaction = True, wait = 3, text = "The Lady is listening to her gramophone in her bedroom"), Path_Tile(4, 13, door = True), 
                                   Path_Tile(1, 1, door = True), Path_Tile(1, 1, interaction = True, wait = 4, text =  "The Lady is admiring the suit of armour in the hallway"), Path_Tile(1, 3), Path_Tile(1, 33, door = True), 
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
                self._set_death_animation()
        else:
            self.pathing.update(game_vars, self)

            # Text timer
            if self.text != None:
                if game_vars.time > self.text.time + self.text.display_time:
                    self.text = None

            
            # Set door exclamation
            if self.key_points[self.pathing.next_key_point_ind].door == True:
                if game_vars.current_room == self.key_points[self.pathing.next_key_point_ind + 1].room:
                    tile = game_vars.room_list[game_vars.current_room].tiles[self.key_points[self.pathing.next_key_point_ind + 1].tile]
                    for o in tile.obj:
                        if o.obj_type == Obj_Type.door:
                            o.danger = True

            # Find body
            for c in game_vars.room_list[self.pathing.current_room].chars:

                if c != self and self.alive:
                    if c.alive == False:
                        game_vars.caught = True

            if self.pathing.timer == None:
                self.pos.x += self.vel.x*game_vars.dt
                self.pos.y += self.vel.y*game_vars.dt

        self.sprites.update(game_vars.time)


    def draw(self, screen):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        
        if self.alive:
            screen.blit(self.sprites.animation_list[self.sprites.ind], rect)

            if self.char == Char.duchess:
                y_offset = 0
            elif self.char == Char.duke or self.char == Char.heir:
                y_offset = 40
            else:
                y_offset = 24

            # Draw exclamation
            if self.can_see_player:
                rect = pygame.Rect(self.pos.x - 12, self.pos.y - self.exclamation.y_cut + y_offset, self.exclamation.x_cut, self.exclamation.y_cut)
                screen.blit(self.exclamation.animation_list[self.exclamation.ind], rect)
                self.can_see_player = False

            # Draw text
            if self.text != None:
                self.text.draw(screen, self.pos.x - self.text.size.x/2 + self.size.x/2, self.pos.y + y_offset - self.text.size.y -10)

            return
        else:
            angle = 180
            rect = pygame.Rect(self.pos.x, self.pos.y + self.size.y/2, self.size.x, self.size.y)
            rotated_image = pygame.transform.rotate(self.sprites.animation_list[self.sprites.ind], angle)

            screen.blit(rotated_image, rect)

    def _set_death_animation(self):

        match self.death_type:
            case Death_Type.explode:
                explode_track = Music_Sound(1, Path("../res/Py_week_Traitor_Sound_Effects/explosion.wav"))
                explode_track.load()
                explode_track.play()

                if self.char == Char.duke:
                    self.sprites.set_animation(32, 32, repeat = False)

                if self.char == Char.lady:
                    self.sprites.set_animation(19, 20, repeat = False)

            case Death_Type.poison:
                poison_track = Music_Sound(1, Path("../res/Py_week_Traitor_Sound_Effects/water_pour.wav"))
                poison_track.load()
                poison_track.play()

                if self.char == Char.duke:
                    self.sprites.set_animation(33, self.animation_steps - 1, repeat = False)

                if self.char == Char.duchess:
                    self.sprites.set_animation(4, self.animation_steps - 1, repeat = False)

            case Death_Type.electrecute:
                electro_track = Music_Sound(1, Path("../res/Py_week_Traitor_Sound_Effects/electrocution.wav"))
                electro_track.load()
                electro_track.play()

                if self.char == Char.lady:
                    self.sprites.set_animation(16, 17, repeat = 10)

                if self.char == Char.heir:
                    self.sprites.set_animation(32, 33, repeat = 10)

            case Death_Type.chop:
                axe_track = Music_Sound(1, Path("../res/Py_week_Traitor_Sound_Effects/Axe.wav"))
                axe_track.load()
                axe_track.play()

                if self.char == Char.lady:
                    self.sprites.set_animation(19, 20, repeat = False)

                if self.char == Char.cleaner:
                    self.sprites.set_animation(35, 36, repeat = False)
        
            case Death_Type.crush:
                bookcase_track = Music_Sound(1, Path("../res/Py_week_Traitor_Sound_Effects/bookcase_fall.wav"))
                bookcase_track.load()
                bookcase_track.play()
                splat_track = Music_Sound(1, Path("../res/Py_week_Traitor_Sound_Effects/splat.wav"))
                splat_track.load()
                splat_track.play()

                if self.char == Char.duchess:
                    self.sprites.set_animation(4, self.animation_steps - 1, repeat = False)


            case Death_Type.fall:
                man_scream_track = Music_Sound(1, Path("../res/Py_week_Traitor_Sound_Effects/death_scream_male.wav"))
                man_scream_track.load()
                man_scream_track.play()
                if self.char == Char.heir:
                    pass

                if self.char == Char.cleaner:
                    pass

 
