from entity import Ent
from input import Input
from object import Obj, Obj_Type
import pygame
from settings import Direction, SPEED, fvec2, TILE_H, TILE_W

class Player(Ent):
    def __init__(self, x_pos: float, y_pos: float):
        filepath = "../res/char.png"
        animation_steps = 32
        self.velocity = fvec2(0, 0)
        self.selected_obj: Obj = None
        self.inventory: Obj = []
        self.prev_dir: Direction = Direction.dl

        self.dl_start = 0
        self.dr_start = 8
        self.ur_start = 16
        self.ul_start = 24

        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, input: Input, game_vars):
        self.velocity = fvec2(0, 0)
        self.prev_dir = self.dir
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
            if self.selected_obj.obj_type  == Obj_Type.door:
                game_vars.current_room = self.selected_obj.new_room
                print(game_vars.current_room)
                self.pos.x = game_vars.room_list[game_vars.current_room].tiles[self.selected_obj.go_to].pos.x + TILE_W/2
                self.pos.y = game_vars.room_list[game_vars.current_room].tiles[self.selected_obj.go_to].pos.y - self.size.y/2
                self.selected_obj.selected = False
                self.selected_obj.sprites.ind -= 1
                self.selected_obj = None

            # If selected object is interactable stationary object
            if self.selected_obj.obj_type == Obj_Type.interact:
                 for i in self.inv:
                    if self.selected_obj.pickup_type = i.pickup_type:
                        print("This object is now deadly")
                        self.selected_obj.active = True
                        self.selected_obj.selected = False
                        self.selected_obj = None
                    else:
                        print("You don't have the right kind of object, dingus")
                
    def draw_inv(self, screen) -> None:
        if len(self.inventory) > 0:
            count = 0
            for i in self.inventory:
                rect = pygame.Rect(10*count + count*i.size.x, 10, i.size.x, i.size.y)
                screen.blit(i.sprites.animation_list[i.sprites.ind], rect)
                count += 1
