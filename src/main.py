from character import Character, Char
from entity import Ent
from input import Input
from object import Obj, Obj_Type, Pickup_Type
from pathlib import Path
from player import Player
import pygame
from room import Room
from settings import Settings, WIDTH, HEIGHT, GameVars

if __name__ == "__main__":
    pygame.init()

    ###this is for the snarky joke im gonna leave in the game
    ##remove once the joke has been done
    ###its blitted at the end of the main function
    meme = pygame.image.load(Path("../res/comment.jpg"))

    settings = Settings()
    ###initialise the game vars
    game_vars = GameVars()

    input = Input()
    prev_input = Input()

    input.prev_input = prev_input
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #temporeroly removed fullscreen as itll be easier for me to find this bug
    #, pygame.FULLSCREEN
    player = Player(300, 300)

    ###initialise some of the rooms to test transitions
    study_room = Room("study", 5, 5)
    study_room.tiles[12].obj.append(Obj(Path("../res/box1.png")))
    study_room.add_walls("../res/windows.png")
    study_room.tiles[20].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.water_bottle))
    study_room.tiles[0].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 3, go_to = 3))


    hallway_room = Room("hallway", 10, 4)
    hallway_room.tiles[12].obj.append(Obj(Path("../res/box1.png")))

    dining_room = Room("dining", 6, 6)
    
    kitchen_room = Room("kitchen", 4, 6)
    kitchen_room.add_walls("../res/kitchen_wall.png")
    kitchen_room.tiles[5].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.water_bottle))
    kitchen_room.tiles[11].obj.append(Obj(Path("../res/usables2.png"), obj_type = Obj_Type.pickup, pickup_type = Pickup_Type.rat_poison))
    kitchen_room.tiles[3].obj.append(Obj(Path("../res/doors.png"), obj_type = Obj_Type.door, new_room = 0, go_to = 0))

    heir = Character(kitchen_room.tiles[0].pos.x, kitchen_room.tiles[0].pos.y - 64, Char.heir)
    duke = Character(kitchen_room.tiles[0].pos.x, kitchen_room.tiles[0].pos.y - 64, Char.duke)
    duchess = Character(kitchen_room.tiles[4].pos.x, kitchen_room.tiles[4].pos.y - 64, Char.duchess)
    cleaner = Character(kitchen_room.tiles[8].pos.x, kitchen_room.tiles[8].pos.y - 64, Char.cleaner)
    lady = Character(kitchen_room.tiles[12].pos.x, kitchen_room.tiles[12].pos.y- 64, Char.lady)
    game_vars.chars = [heir, duke, duchess, cleaner, lady]
    kitchen_room.chars = [heir, duke, duchess, cleaner, lady]


    game_vars.room_list = [study_room, hallway_room, dining_room, kitchen_room]
    game_vars.current_room = 3

    while settings.running:
        game_vars.time = pygame.time.get_ticks()

        screen.fill((128, 128, 128))

        input.update(settings, prev_input)
        game_vars.room_list[game_vars.current_room].set_interact(player)
        player.update(input, game_vars)

        for i in game_vars.chars:
            i.update(game_vars)        
        ###this goes over the list of rooms, checks which room the player (in the game vars) is in against the names of the rooms
        game_vars.room_list[game_vars.current_room].draw(screen, player)
        player.draw_inv(screen)

        ###this is where I blit the image to the screen, the image is leaded at the begining of the main function
        ###can remove once done
        #screen.blit(meme, (0, 0))

        pygame.display.update()