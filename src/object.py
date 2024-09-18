from entity import Ent
from enum import Enum
from settings import TILE_H

Obj_Type = Enum("Obj_type", ["wall", "door", "pickup", "interact", "other"])
Pickup_Type = Enum("Pickup_Type", ["water_bottle", "rat_poison", "banana", "screwdriver", "will"])
Interact_Type = Enum("interact_type", ["stove", "whiskey", "wine", "gramophone", "armour", "telephone", "bookshelf"])


class Obj(Ent):
    def __init__(self, filepath: str,  ind: int = 0, obj_type: Obj_Type = Obj_Type.other, pickup_type: Pickup_Type = None, new_room: int = None, go_to: int = None):
        self.obj_type = obj_type
        self.go_to = None
        self.selected = False
        self.pickup_type = None
        self.interact_type = None

        match self.obj_type:
            case Obj_Type.wall: 
                animation_steps = 2
                self.collide = False
                self.interact = False

            case Obj_Type.door:
                animation_steps = 4
                self.collide = False
                self.interact = True
                self.new_room = new_room
                self.go_to = go_to

            case Obj_Type.pickup:
                animation_steps = 10
                self.collide = False
                self.interact = True
                self.pickup_type = pickup_type

                match self.pickup_type:
                    case Pickup_Type.water_bottle:
                        ind = 0

                    case Pickup_Type.rat_poison:
                        ind = 2

            case Obj_Type.interact:
                animation_steps = 7
                self.collide = True
                self.interact = True

                match self.interact_type:

                    case Interact_Type.stove:
                        ind = 0
                        self.pickup_type = None

                    case Interact_Type.whiskey:
                        ind = 1
                        self.pickup_type = [Pickup_Type.rat_poison]

                    case Interact_Type.wine:
                        ind = 2
                        self.pickup_type = [Pickup_Type.rat_poison]

                    case Interact_Type.gramophone:
                        ind = 3
                        self.pickup_type = [Pickup_Type.water_bottle, Pickup_Type.screwdriver]

                    case Interact_Type.armour:
                        ind = 4
                        self.pickup_type = [Pickup_Type.screwdriver]

                    case Interact_Type.telephone:
                        ind = 5
                        self.pickup_type = [Pickup_Type.water_bottle]

                    case Interact_Type.bookshelf:
                        ind = 6
                        self.pickup_type = [Pickup_Type.screwdriver]

            case Obj_Type.other:
                animation_steps = 1
                self.collide = True
                self.interact = False
        
        
        x_pos = 0
        y_pos = 0
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)
