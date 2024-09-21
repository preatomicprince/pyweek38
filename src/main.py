from character import Character, Char
from entity import Ent
from input import Input
from object import Obj, Obj_Type, Pickup_Type, Interact_Type, Decor_Type
from pathlib import Path
from player import Player
import pygame
from room import Room
from ui import *
from settings import Settings, GameVars
from typedefs import WIDTH, HEIGHT

def main(settings: Settings, screen):

    ###initialise the game vars
    game_vars = GameVars()

    input = Input()
    prev_input = Input()

    input.prev_input = prev_input
    
    player = Player(400, 300)

    ###initialising for the UI

    play_but = Buttons(20, 20, 2, "play")
    exit_but = Buttons(120, 20, 4, "exit")
    restart_but = Buttons(220, 20, 6, "restart")

    button_list = [play_but, exit_but, restart_but]

    ###initialise some of the rooms to test transitions
    study_room = Room("study", 5, 5)
    study_room.add_walls("../res/kitchen_wall.png")
    study_room.tiles[21].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.screwdriver))
    study_room.tiles[19].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 20))
    study_room.tiles[0].obj.append(Obj(ind = 1, obj_type=Obj_Type.decor, decor_type=Decor_Type.bookcase))
    study_room.tiles[5].obj.append(Obj(ind = 1, obj_type=Obj_Type.decor, decor_type=Decor_Type.bookcase))
    study_room.tiles[10].obj.append(Obj(Path("../res/windows.png/"), ind = 1, obj_type = Obj_Type.wall))
    study_room.tiles[15].obj.append(Obj(ind = 1, obj_type=Obj_Type.decor, decor_type=Decor_Type.bookcase))
    study_room.tiles[20].obj.append(Obj(ind = 1, obj_type=Obj_Type.decor, decor_type=Decor_Type.bookcase))


    hallway_room = Room("hallway", 10, 4)
    hallway_room.add_walls("../res/hall_way_walls.png")
    # bedroom1 door
    hallway_room.tiles[1].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 4, go_to = 13))
    # bedroom2 door
    hallway_room.tiles[5].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 5, go_to = 14))
    # living_room door
    hallway_room.tiles[6].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 6, go_to = 16))
    # library door
   # hallway_room.tiles[9].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 7, go_to = 14))
    # kitchen_room door
    hallway_room.tiles[33].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 3, go_to = 3))
    # study_room door
    hallway_room.tiles[20].obj.append(Obj(Path("../res/doors.png"), ind = 2, obj_type = Obj_Type.door, new_room = 0, go_to = 19))
    # dining_room door
    hallway_room.tiles[37].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 2, go_to = 1))
    hallway_room.tiles[35].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.telephone))
    hallway_room.tiles[0].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.armour))


    dining_room = Room("dining", 6, 6)
    dining_room.add_walls("../res/dining.wall.png")
    # kitchen door
    dining_room.tiles[12].obj.append(Obj(Path("../res/doors.png"), ind = 2, obj_type = Obj_Type.door, new_room = 3, go_to = 11))
    # hallway door
    dining_room.tiles[1].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 37))
    dining_room.tiles[4].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.whiskey))
    dining_room.tiles[14].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.banana))



    bedroom1 = Room("bedroom1", 3, 5)
    bedroom1.add_walls("../res/kitchen_wall.png")
    # hallway_room door
    bedroom1.tiles[13].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 1))
    bedroom1.tiles[1].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.gramophone))

    
    bedroom2 = Room("bedroom2", 3, 5)
    bedroom2.add_walls("../res/kitchen_wall.png")
    bedroom2.tiles[1].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.window))

    # hallway_room door
    bedroom2.tiles[14].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 5))
    bedroom2.tiles[4].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.water_bottle))

    living_room = Room("living_room", 4,5)
    living_room.add_walls("../res/kitchen_wall.png")
    # library door
    living_room.tiles[11].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 7, go_to = 6))
    # hallway_room door
    living_room.tiles[16].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 6))
    living_room.tiles[0].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.wine))



    library = Room("library", 3, 5)
    library.add_walls("../res/kitchen_wall.png")
    # living_room door
    library.tiles[6].obj.append(Obj(Path("../res/doors.png"), ind = 2, obj_type = Obj_Type.door, new_room = 6, go_to = 11))
    library.tiles[12].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.bookshelf))
    library.tiles[1].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.window))
    library.tiles[0].obj.append(Obj(ind = 1, obj_type=Obj_Type.decor, decor_type=Decor_Type.bookcase))
    library.tiles[3].obj.append(Obj(ind = 1, obj_type=Obj_Type.decor, decor_type=Decor_Type.bookcase))




    # hallway_room door
    #library.tiles[14].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 9))


    kitchen_room = Room("kitchen", 4, 6)
    kitchen_room.add_walls("../res/kitchen_wall.png")
    kitchen_room.tiles[1].obj.append(Obj(obj_type = Obj_Type.interact, interact_type = Interact_Type.stove))
    kitchen_room.tiles[12].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.rat_poison))
    # hallway_room door
    kitchen_room.tiles[3].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 1, go_to = 33))
    # dining_room door
    kitchen_room.tiles[11].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 2, go_to = 12))
    kitchen_room.tiles[0].obj.append(Obj(ind = 0, obj_type=Obj_Type.decor, decor_type=Decor_Type.counter))
    kitchen_room.tiles[2].obj.append(Obj(ind = 0, obj_type=Obj_Type.decor, decor_type=Decor_Type.counter))
    kitchen_room.tiles[4].obj.append(Obj(Path("../res/windows.png/"), ind = 1, obj_type = Obj_Type.wall))

    kitchen_room.tiles[4].obj.append(Obj(ind = 3, obj_type=Obj_Type.decor, decor_type=Decor_Type.counter))
    kitchen_room.tiles[8].obj.append(Obj(ind = 3, obj_type=Obj_Type.decor, decor_type=Decor_Type.counter))
    kitchen_room.tiles[16].obj.append(Obj(ind = 3, obj_type=Obj_Type.decor, decor_type=Decor_Type.counter))


    heir = Character(bedroom2.tiles[0].pos.x, bedroom2.tiles[0].pos.y, Char.heir)
    duke = Character(kitchen_room.tiles[5].pos.x, kitchen_room.tiles[5].pos.y, Char.duke)
    duchess = Character(living_room.tiles[4].pos.x, living_room.tiles[4].pos.y, Char.duchess)
    cleaner = Character(library.tiles[13].pos.x , library.tiles[13].pos.y, Char.cleaner)
    lady = Character(bedroom1.tiles[2].pos.x , bedroom1.tiles[2].pos.y, Char.lady)

    game_vars.chars = [heir, duke, duchess, cleaner, lady]

    kitchen_room.chars = [duke]
    bedroom1.chars = [lady]
    bedroom2.chars = [heir]
    library.chars = [cleaner]
    living_room.chars = [duchess]

    game_vars.room_list = [study_room, hallway_room, dining_room, kitchen_room, bedroom1, bedroom2, living_room, library]
    game_vars.current_room = 3

    duke.pathing._set_direction(game_vars, duke)
    lady.pathing._set_direction(game_vars, lady)
    duchess.pathing._set_direction(game_vars, duchess)
    cleaner.pathing._set_direction(game_vars, cleaner)
    heir.pathing._set_direction(game_vars, heir)

    while settings.running:
        screen.fill((0, 0, 0))
        
        game_vars.dt = (pygame.time.get_ticks() - game_vars.time)/1000
        game_vars.time = pygame.time.get_ticks()

        game_vars.set_win_state()

        if game_vars.win:
            # Win state here
            print("You won!")

        if game_vars.caught:
            # Fail state here
            print("You lost!")

        if game_vars.win == False and game_vars.caught == False:
            input.update(button_list, settings, prev_input)
            game_vars.room_list[game_vars.current_room].set_interact(game_vars, player)
            player.update(input, game_vars)

            for i in game_vars.chars:
                i.update(game_vars)  

            game_vars.text_events.update(game_vars)
                  
        ###this goes over the list of rooms, checks which room the player (in the game vars) is in against the names of the rooms
        game_vars.room_list[game_vars.current_room].draw(screen, player)
        player.draw_inv(screen)
        game_vars.text_events.draw(screen)

        for b in button_list:
            b.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)

    while settings.restart:
        settings.running = True
        settings.restart = False
        main(settings, screen)