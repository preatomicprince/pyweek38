from entity import Ent
from input import Input
from object import Obj
from pathlib import Path
from player import Player
import pygame
from room import Room
from settings import Settings, WIDTH, HEIGHT, GameVars

if __name__ == "__main__":
    pygame.init()
    settings = Settings()
    ###initialise the game vars
    game_vars = GameVars()

    input = Input()
    prev_input = Input()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #temporeroly removed fullscreen as itll be easier for me to find this bug
    #, pygame.FULLSCREEN
    player = Player(200, 200)

    ###initialise some of the rooms to test transitions
    study_room = Room("study", 5, 5)
    study_room.tiles[12].obj.append(Obj(Path("../res/box1.png")))

    hallway_room = Room("hallway", 10, 4)
    hallway_room.tiles[12].obj.append(Obj(Path("../res/box1.png")))

    dining_room = Room("dining", 6, 6)
    
    kitchen_room = Room("kitchen", 4, 6)
    for c in range(kitchen_room.rows):

        kitchen_room.tiles[c].obj.append(Obj("../res/windows.png", animation_steps=2, ind=0))
    for c in range(kitchen_room.cols):
        for r in range(kitchen_room.rows):
            if c == 0:
                kitchen_room.tiles[c*kitchen_room.rows + r].obj.append(Obj("../res/kitchen_wall.png", animation_steps=2, ind=0)) 
            if r == 0:
                kitchen_room.tiles[c*kitchen_room.rows + r].obj.append(Obj("../res/kitchen_wall.png", animation_steps=2, ind=1))    


        ##kitchen_room.tiles[c].obj.append(Obj("../res/kitchen_wall.png", animation_steps=2, ind=0))
        ###0, 4, 8, 12
        ##for r in range(kitchen_room.cols+1 * kitchen_room.rows+1):
          #  if r == kitchen_room.rows:
            #    kitchen_room.tiles[r].obj.append(Obj("../res/kitchen_wall.png", animation_steps=2, ind=1))            
        for c in range(kitchen_room.cols):
            for r in range(kitchen_room.rows):
                if c == 0:
                    kitchen_room.tiles[c*kitchen_room.rows + r].obj.append(Obj("../res/kitchen_wall.png", animation_steps=2, ind=0)) 
                if r == 0:
                    kitchen_room.tiles[c*kitchen_room.rows + r].obj.append(Obj("../res/kitchen_wall.png", animation_steps=2, ind=1))             
        
        #for r in range(kitchen_room.cols):    
            #print(c, r)
            #if r == 3 or c == 0:
                
            
                
            


    room_list = [study_room, hallway_room, dining_room, kitchen_room]

    while settings.running:
        screen.fill((128, 128, 128))

        input.update(settings, prev_input)
        player.update(input)
        
        ###this goes over the list of rooms, checks which room the player (in the game vars) is in against the names of the rooms
        for r in range(len(room_list)):
            if room_list[r].room_name == game_vars.current_room:
                room_list[r].draw(screen, player)

        pygame.display.update()