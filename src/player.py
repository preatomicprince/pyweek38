from entity import Ent
from input import Input
from object import Obj, Obj_Type
import pygame
from settings import Direction, SPEED, fvec2, TILE_H, TILE_W

class Player(Ent):
    def __init__(self, x_pos: float, y_pos: float):
        filepath = "../res/pc.png"
        animation_steps = 1
        self.velocity = fvec2(0, 0)
        self.selected_obj: Obj = None
        self.inventory: Obj = []
        super().__init__(x_pos, y_pos, filepath, animation_steps)

    def update(self, input: Input, game_vars):
        self.velocity = fvec2(0, 0)

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
                self.velocity.x += SPEED.x
                self.velocity.y += SPEED.y

            case Direction.ul:
                self.velocity.x -= SPEED.x
                self.velocity.y -= SPEED.y

            case Direction.ur:
                self.velocity.x += SPEED.x
                self.velocity.y -= SPEED.y

            case Direction.dl:
                self.velocity.x -= SPEED.x
                self.velocity.y += SPEED.y

     
        if input.key_right or input.key_left or input.key_up or input.key_down:
            self.pos.x += self.velocity.x
            self.pos.y += self.velocity.y

        if input.key_interact:
            self.interact(game_vars)

    def get_bottom_pos(self) -> fvec2:
        return fvec2(self.pos.x + self.size.x/2, self.pos.y + self.size.y - 10)

    def interact(self, game_vars) -> None:
        if self.selected_obj != None:
            if self.selected_obj.obj_type == Obj_Type.pickup:
                self.inventory.append(self.selected_obj)
                self.inventory[len(self.inventory)-1].sprites.ind -= 1
                for t in game_vars.current_room.tiles:
                    if t.obj != None:
                        if self.selected_obj in t.obj:
                            t.obj.remove(self.selected_obj)
                self.selected_obj = None
                return
            
            if self.selected_obj.obj_type  == Obj_Type.door:
                game_vars.current_room = game_vars.room_list[self.selected_obj.new_room]
                self.pos.x = game_vars.current_room.tiles[self.selected_obj.go_to].pos.x + TILE_W/2
                self.pos.y = game_vars.current_room.tiles[self.selected_obj.go_to].pos.y - self.size.y/2
                self.selected_obj = None

    def draw_inv(self, screen) -> None:
        if len(self.inventory) > 0:
            count = 0
            for i in self.inventory:
                rect = pygame.Rect(10*count + count*i.size.x, 10, i.size.x, i.size.y)
                screen.blit(i.sprites.animation_list[i.sprites.ind], rect)
                count += 1
