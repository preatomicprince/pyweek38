from entity import Ent
from input import Input
import math
from object import Obj, Obj_Type, Interact_Type, Pickup_Type, Death_Type
import pygame
from settings import Direction, SPEED, fvec2, TILE_H, TILE_W, WIDTH

# DEBUG - Should be False for release
show_tile = False

class Player(Ent):
    def __init__(self, x_pos: float, y_pos: float):
        filepath = "../res/char.png"
        animation_steps = 32
        self.velocity = fvec2(0, 0)
        self.selected_obj: Obj = None
        self.inventory: Obj = []
        self.prev_dir: Direction = Direction.dl
        self.dir = Direction.dr

        self.dl_start = 0
        self.dr_start = 8
        self.ur_start = 16
        self.ul_start = 24

        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, input: Input, game_vars):
        self.velocity = fvec2(0, 0)
        self.prev_dir = self.dir
        
        # For debugging to easily find tile stood on
        if show_tile:
            bp = None
            bp = game_vars.room_list[game_vars.current_room].find_ent_tile(self)

            print(bp)

        if input.key_right:
            self.dir = Direction.dr

        if input.key_left:
            self.dir = Direction.ul

        if input.key_up:
            self.dir = Direction.ur

        if input.key_down:
            self.dir = Direction.dl

        match self.dir:
            case Direction.dr:
                if self.dir != self.prev_dir:
                    self.sprites.set_animation(self.dr_start, self.ur_start - 1)
                self.velocity.x += SPEED.x
                self.velocity.y += SPEED.y

            case Direction.ul:
                if self.dir != self.prev_dir:
                    self.sprites.set_animation(self.ul_start, self.sprites.animation_steps -1)
                self.velocity.x -= SPEED.x
                self.velocity.y -= SPEED.y

            case Direction.ur:
                if self.dir != self.prev_dir:
                    self.sprites.set_animation(self.ur_start, self.ul_start -1)
                self.velocity.x += SPEED.x
                self.velocity.y -= SPEED.y

            case Direction.dl:
                if self.dir != self.prev_dir:
                    self.sprites.set_animation(self.dl_start, self.dr_start -1)
                self.velocity.x -= SPEED.x
                self.velocity.y += SPEED.y

     
        if input.key_right or input.key_left or input.key_up or input.key_down:
            self.sprites.update(game_vars.time)

            self.pos.x += self.velocity.x
            self.pos.y += self.velocity.y

            if self._check_collision(game_vars):
                self.pos.x -= self.velocity.x
                self.pos.y -= self.velocity.y
    
        if input.key_interact:
            if input.prev_input.key_interact == False:
                self.interact(game_vars)

    def _check_collision(self, game_vars):
        return self._wall_collision(game_vars) or self._obj_collision(game_vars)

    def _wall_collision(self, game_vars):

        # Thanks again to https://clintbellanger.net/articles/isometric_math/ 
        cols = game_vars.room_list[game_vars.current_room].cols
        rows = game_vars.room_list[game_vars.current_room].rows

        pti = game_vars.room_list[game_vars.current_room].find_ent_tile(self)
        if pti != None:
            pt = game_vars.room_list[game_vars.current_room].ind_to_coord(pti)
            if pt.x != 0 and pt.x != rows and pt.y != 0 and pt.y != cols:
                return False
            
        if game_vars.current_room == 0:
            mapx = ((self.pos.x / (TILE_W/2 )) + (self.pos.y / (TILE_H/2)))/2 - cols - .5
            mapy = ((self.pos.y / (TILE_H/2 )) - (self.pos.x / (TILE_W/2)))/2 + 1

        elif game_vars.current_room == 1:
            mapx = ((self.pos.x / (TILE_W/2 )) + (self.pos.y / (TILE_H/2)))/2 - cols - 3
            mapy = ((self.pos.y / (TILE_H/2 )) - (self.pos.x / (TILE_W/2)))/2 + 2.5

        # Dunno why some rooms have a slight map position offset. 
        # No time to figure it out but this makes it work properly
        
        elif game_vars.current_room == 3:
            mapx = ((self.pos.x / (TILE_W/2 )) + (self.pos.y / (TILE_H/2)))/2 - cols + 1
            mapy = ((self.pos.y / (TILE_H/2 )) - (self.pos.x / (TILE_W/2)))/2 + .5
        elif game_vars.current_room == 2:
            mapx = ((self.pos.x / (TILE_W/2 )) + (self.pos.y / (TILE_H/2)))/2 - cols + 0.5
            mapy = ((self.pos.y / (TILE_H/2 )) - (self.pos.x / (TILE_W/2)))/2 + 1
        else:
            mapx = ((self.pos.x / (TILE_W/2 )) + (self.pos.y / (TILE_H/2)))/2 - cols
            mapy = ((self.pos.y / (TILE_H/2 )) - (self.pos.x / (TILE_W/2)))/2 + .5
        if mapx < 0 or mapx > cols:
            return True

        if mapy < 0 or mapy > rows:
            return True
        
        return False

    def _obj_collision(self, game_vars):

        pti = game_vars.room_list[game_vars.current_room].find_ent_tile(self)
        if pti != None:
            if len(game_vars.room_list[game_vars.current_room].tiles[pti].obj) > 0:
                for o in game_vars.room_list[game_vars.current_room].tiles[pti].obj:
                    if o.collide:
                        return True
                
        return False

    def interact(self, game_vars) -> None:
        
        # Check if there's a body to clear
        if len(game_vars.room_list[game_vars.current_room].chars) > 0:
            for c in game_vars.room_list[game_vars.current_room].chars:
                if c.alive == False:
                    rows = game_vars.room_list[game_vars.current_room].rows
                    cti = game_vars.room_list[game_vars.current_room].find_ent_tile(c)
                    pti = game_vars.room_list[game_vars.current_room].find_ent_tile(self)
                    check_tiles = [pti, pti - 1, pti + 1, pti - rows, pti + rows]
                    for t in check_tiles:
                        if t == cti:
                            game_vars.room_list[game_vars.current_room].chars.remove(c)
                            print("Body hidden!")
            return
        
        if self.selected_obj != None:

            # If selected object is a pickup
            if self.selected_obj.obj_type == Obj_Type.pickup:
                self.inventory.append(self.selected_obj)
                self.inventory[len(self.inventory)-1].sprites.ind -= 1
                for t in game_vars.room_list[game_vars.current_room].tiles:
                    if t.obj != None:
                        if self.selected_obj in t.obj:
                            t.obj.remove(self.selected_obj)
                self.selected_obj = None
                self._check_if_caught(game_vars)
                return
            
            # If selected object is door
            elif self.selected_obj.obj_type == Obj_Type.door:
                game_vars.current_room = self.selected_obj.new_room
                self.pos.x = game_vars.room_list[game_vars.current_room].tiles[self.selected_obj.go_to].pos.x + TILE_W/2 - self.size.x/2
                self.pos.y = game_vars.room_list[game_vars.current_room].tiles[self.selected_obj.go_to].pos.y + 20 + TILE_H/2 - self.size.y
                self.selected_obj.selected = False
                self.selected_obj.sprites.ind -= 1
                self.selected_obj = None
                return

            # If selected object is interactable stationary object
            elif self.selected_obj.obj_type == Obj_Type.interact:
                 
                # Special case for stove, that doesn't require any pickup to interact
                if self.selected_obj.interact_type == Interact_Type.stove:
                    self._check_if_caught(game_vars)
                    self.selected_obj.interact = False
                    self.selected_obj.active = True
                    self.selected_obj.selected = False
                    self.selected_obj = None
                    return
                
                    

                # All other interact objects
                for i in self.inventory:
                    for p in self.selected_obj.pickup_type:
                        if p == i.pickup_type:
                            #special case for gramophone with 2 ways to kill
                            if self.selected_obj.interact_type == Interact_Type.gramophone:
                                if p == Pickup_Type.screwdriver:
                                    self.selected_obj.death_type = Death_Type.explode

                                elif p == Pickup_Type.water_bottle:
                                    self.selected_obj.death_type = Death_Type.electrecute

                            print("This object is now deadly")
                            self._check_if_caught(game_vars)
                            self.inventory.remove(i)
                            self.selected_obj.interact = False
                            self.selected_obj.active = True
                            self.selected_obj.selected = False
                            self.selected_obj = None
                            return
                        
                # Code below will run if player doesn't have correct pickup
                print("You don't have the right kind of object, dingus")
                
    def draw_inv(self, screen) -> None:
        if len(self.inventory) > 0:
            count = 0
            for i in self.inventory:
                rect = pygame.Rect(10*count + count*i.size.x, 10, i.size.x, i.size.y)
                screen.blit(i.sprites.animation_list[i.sprites.ind], rect)
                count += 1

    def _check_if_caught(self, game_vars):
        # Checks if player is caught

        ###add a bark here
        if len(game_vars.room_list[game_vars.current_room].chars) > 0:
            for c in game_vars.room_list[game_vars.current_room].chars:

                # Check if character is too close to charcter
                char_coord = game_vars.room_list[game_vars.current_room].ind_to_coord(c.pathing.current_tile)
                player_ind = game_vars.room_list[game_vars.current_room].find_ent_tile(self)
                player_coord = game_vars.room_list[game_vars.current_room].ind_to_coord(player_ind)
                
                caught = False

                if char_coord.x - 2 < player_coord.x < char_coord.x + 2:
                    if char_coord.y - 2 < player_coord.y < char_coord.y + 2:
                        caught = True
                
                match c.dir:
                    case Direction.dl:
                        if player_coord.y > char_coord.y:
                            caught = True
                    
                    case Direction.ur:
                        if player_coord.y < char_coord.y:
                            caught = True

                    case Direction.ul:
                        if player_coord.x < char_coord.x:
                            caught = True
                    
                    case Direction.dr:
                        if player_coord.x > char_coord.x:
                            caught = True

                if caught:
                    print("Caught")