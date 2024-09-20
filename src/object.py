from entity import Ent
from enum import Enum
from pathlib import Path
from settings import TILE_H

Obj_Type = Enum("Obj_type", ["wall", "door", "pickup", "interact", "decor", "other"])
Pickup_Type = Enum("Pickup_Type", ["water_bottle", "rat_poison", "banana", "screwdriver", "will"])
Interact_Type = Enum("interact_type", ["stove", "whiskey", "wine", "gramophone", "armour", "telephone", "bookshelf", "window"])
Death_Type = Enum("Death_Type", ["explode", "poison", "electrecute", "chop", "crush", "fall"])
Decor_Type = Enum("Decor_Type", ["bookcase", "counter"])


class Obj(Ent):
    def __init__(self, filepath: str = None,  ind: int = 0, 
                 obj_type: Obj_Type = Obj_Type.other, 
                 interact_type: Interact_Type = None, pickup_type: Pickup_Type = None, decor_type: Decor_Type = None,
                 new_room: int = None, go_to: int = None):
        
        self.obj_type = obj_type
        self.go_to = None
        self.selected = False
        self.pickup_type = None
        self.decor_type = decor_type
        self.death_type = None
        self.interact_type = interact_type
        self.active = None

        match self.obj_type:
            case Obj_Type.wall:
                animation_steps = 2
                self.collide = False
                self.interact = False

            case Obj_Type.door:
                filepath = Path("../res/doors.png")
                animation_steps = 4
                self.collide = False
                self.interact = True
                self.new_room = new_room
                self.danger = False
                self.go_to = go_to

            case Obj_Type.pickup:
                filepath = Path("../res/usables2.png")
                animation_steps = 10
                self.collide = False
                self.interact = True
                self.pickup_type = pickup_type

                match self.pickup_type:
                    case Pickup_Type.water_bottle:
                        ind = 0

                    case Pickup_Type.rat_poison:
                        ind = 2

                    case Pickup_Type.banana:
                        ind = 4

                    case Pickup_Type.screwdriver:
                        ind = 6

            case Obj_Type.interact:
                filepath = Path("../res/interact.png")
                animation_steps = 14
                self.collide = False
                self.interact = True

                # If the correct pickup has been used
                self.active = False

                match self.interact_type:

                    case Interact_Type.stove:
                        self.collide = True
                        ind = 0
                        self.pickup_type = []

                    case Interact_Type.whiskey:
                        ind = 2
                        self.pickup_type = [Pickup_Type.rat_poison]

                    case Interact_Type.wine:
                        ind = 4
                        self.pickup_type = [Pickup_Type.rat_poison]

                    case Interact_Type.gramophone:
                        self.collide = True
                        ind = 6
                        self.pickup_type = [Pickup_Type.water_bottle, Pickup_Type.screwdriver]

                    case Interact_Type.armour:
                        self.collide = True
                        ind = 8
                        self.pickup_type = [Pickup_Type.screwdriver]

                    case Interact_Type.telephone:
                        self.collide = True
                        ind = 10
                        self.pickup_type = [Pickup_Type.water_bottle]

                    case Interact_Type.bookshelf:
                        self.collide = True
                        animation_steps = 4
                        filepath = Path("../res/bookcase.png")
                        ind = 2
                        self.pickup_type = [Pickup_Type.screwdriver]

                    case Interact_Type.window:
                        ind = 0
                        animation_steps = 2
                        filepath = Path("../res/open_window2.png")
                        self.pickup_type = [Pickup_Type.banana]

            case Obj_Type.decor:
                self.collide = True
                self.interact = False

                match self.decor_type:
                    case Decor_Type.bookcase:
                        filepath = Path("../res/bookcase.png")
                        animation_steps = 4

                    case Decor_Type.counter:
                        filepath = Path("../res/counter.png")
                        animation_steps = 4

            case Obj_Type.other:
                animation_steps = 1
                self.collide = True
                self.interact = False
        
        
        x_pos = 0
        y_pos = 0
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)
