from entity import Ent
from input import Input
from object import Obj, Obj_Type, Interact_Type, Pickup_Type, Death_Type
import pygame
from settings import Direction, SPEED, fvec2, TILE_H, TILE_W

show_tile = True

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

        if input.key_interact:
            if input.prev_input.key_interact == False:
                self.interact(game_vars)


    def interact(self, game_vars) -> None:
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
                return
            
            # If selected object is door
            elif self.selected_obj.obj_type == Obj_Type.door:
                game_vars.current_room = self.selected_obj.new_room
                self.pos.x = game_vars.room_list[game_vars.current_room].tiles[self.selected_obj.go_to].pos.x + TILE_W/2
                self.pos.y = game_vars.room_list[game_vars.current_room].tiles[self.selected_obj.go_to].pos.y - self.size.y/2
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