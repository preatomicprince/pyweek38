from character import Character, Char
from entity import Ent
from input import Input
from object import Obj, Obj_Type, Pickup_Type, Interact_Type
from pathlib import Path
from player import Player
import pygame
from room import Room
from ui import *
from settings import Settings, WIDTH, HEIGHT, GameVars, TILE_W, TILE_H

# Just here so the "comment" splashscreen isn't in the way during my testing
from sys import platform

if __name__ == "__main__":
    pygame.init()

    # to-do: add comment
    meme = pygame.image.load(Path("../res/1lzym5zv16j01.png"))

    settings = Settings()
    ###initialise the game vars
    game_vars = GameVars()

    input = Input()
    prev_input = Input()

    input.prev_input = prev_input
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #temporeroly removed fullscreen as itll be easier for me to find this bug
    #, pygame.FULLSCREEN
    player = Player(400, 300)

    ###initialising for the UI

    play_but = Buttons(20, 20, 2, "play")
    exit_but = Buttons(120, 20, 4, "exit")
    restart_but = Buttons(220, 20, 6, "restart")

    button_list = [play_but, exit_but, restart_but]

    ###initialise some of the rooms to test transitions
    study_room = Room("study", 5, 5)
    study_room.add_walls("../res/kitchen_wall.png")
    #study_room.tiles[20].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.water_bottle))
    study_room.tiles[9].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 10))

    hallway_room = Room("hallway", 10, 4)
    hallway_room.add_walls("../res/hall_way_walls.png")
    # bedroom1 door
    hallway_room.tiles[2].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 4, go_to = 14))
    # bedroom2 door
    hallway_room.tiles[5].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 5, go_to = 14))
    # living_room door
    hallway_room.tiles[6].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 6, go_to = 16))
    # library door
    hallway_room.tiles[9].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 7, go_to = 14))
    # kitchen_room door
    hallway_room.tiles[33].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 3, go_to = 3))
    # study_room door
    hallway_room.tiles[20].obj.append(Obj(Path("../res/doors.png"), ind = 1, obj_type = Obj_Type.door, new_room = 0, go_to = 9))
    # dining_room door
    hallway_room.tiles[37].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 2, go_to = 1))
    hallway_room.tiles[35].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.telephone))
    hallway_room.tiles[0].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.armour))


    dining_room = Room("dining", 6, 6)
    dining_room.add_walls("../res/dining.wall.png")
    # kitchen door
    dining_room.tiles[12].obj.append(Obj(Path("../res/doors.png"), ind = 1, obj_type = Obj_Type.door, new_room = 3, go_to = 11))
    # hallway door
    dining_room.tiles[1].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 37))
    dining_room.tiles[4].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.whiskey))


    bedroom1 = Room("bedroom1", 3, 5)
    bedroom1.add_walls("../res/kitchen_wall.png")
    # hallway_room door
    bedroom1.tiles[14].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 2))
    bedroom1.tiles[1].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.gramophone))

    
    bedroom2 = Room("bedroom2", 3, 5)
    bedroom2.add_walls("../res/kitchen_wall.png")
    bedroom2.tiles[1].obj.append(Obj(Path("../res/windows.png/"), ind = 0, obj_type = Obj_Type.wall))
    # hallway_room door
    bedroom2.tiles[14].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 5))
    bedroom2.tiles[4].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.water_bottle))

    living_room = Room("living_room", 4,5)
    living_room.add_walls("../res/kitchen_wall.png")
    # library door
    living_room.tiles[11].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 7, go_to = 6))
    # hallway_room door
    living_room.tiles[16].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 6))


    library = Room("library", 3, 5)
    library.add_walls("../res/kitchen_wall.png")
    # living_room door
    library.tiles[6].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 6, go_to = 11))
    library.tiles[12].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.bookshelf))
    library.tiles[1].obj.append(Obj(Path("../res/windows.png/"), ind = 0, obj_type = Obj_Type.wall))

    # hallway_room door
    library.tiles[14].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 9))


    kitchen_room = Room("kitchen", 4, 6)
    kitchen_room.add_walls("../res/kitchen_wall.png")
    kitchen_room.tiles[8].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.stove))
    kitchen_room.tiles[12].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.rat_poison))
    # hallway_room door
    kitchen_room.tiles[3].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 33))
    # dining_room door
    kitchen_room.tiles[11].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 2, go_to = 12))

    #heir = Character(kitchen_room.tiles[0].pos.x, kitchen_room.tiles[0].pos.y - 64, Char.heir)
    duke = Character(kitchen_room.tiles[21].pos.x, kitchen_room.tiles[21].pos.y - TILE_H, Char.duke)

    duchess = Character(living_room.tiles[4].pos.x, living_room.tiles[4].pos.y, Char.duchess)
    #cleaner = Character(kitchen_room.tiles[8].pos.x, kitchen_room.tiles[8].pos.y - 64, Char.cleaner)
    lady = Character(bedroom1.tiles[2].pos.x , bedroom1.tiles[2].pos.y, Char.lady)
    #game_vars.chars = [heir, duke, duchess, cleaner, lady]
    #kitchen_room.chars = [heir, duke, duchess, cleaner, lady]
    game_vars.chars = [duke, lady, duchess]
    kitchen_room.chars = [duke]
    bedroom1.chars = [lady]
    living_room.chars = [duchess]

    game_vars.room_list = [study_room, hallway_room, dining_room, kitchen_room, bedroom1, bedroom2, living_room, library]
    game_vars.current_room = 3

    duke.pathing._set_direction(game_vars, duke)
    lady.pathing._set_direction(game_vars, lady)
    duchess.pathing._set_direction(game_vars, duchess)

    while settings.running:
        game_vars.time = pygame.time.get_ticks()

        screen.fill((128, 128, 128))

        input.update(button_list, settings, prev_input)
        game_vars.room_list[game_vars.current_room].set_interact(player)
        player.update(input, game_vars)

        for i in game_vars.chars:
            i.update(game_vars)  
                  
        ###this goes over the list of rooms, checks which room the player (in the game vars) is in against the names of the rooms
        game_vars.room_list[game_vars.current_room].draw(screen, player)
        player.draw_inv(screen)

        ###this is where I blit the image to the screen, the image is leaded at the begining of the main function
        ###can remove once done
        #if platform == "linux":
           #screen.blit(meme, (0, 0))
        for b in button_list:
            b.draw(screen)
        pygame.display.update()