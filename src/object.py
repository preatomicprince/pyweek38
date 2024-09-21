from entity import Ent
from enum import Enum
from pathlib import Path
from text import Text
from music import Music_Sound
Obj_Type = Enum("Obj_type", ["wall", "door", "pickup", "interact", "decor", "other"])
Pickup_Type = Enum("Pickup_Type", ["water_bottle", "rat_poison", "banana", "screwdriver", "will"])
Interact_Type = Enum("interact_type", ["stove", "whiskey", "wine", "gramophone", "armour", "telephone", "bookshelf", "window"])
Death_Type = Enum("Death_Type", ["explode", "poison", "electrecute", "chop", "crush", "fall"])
Decor_Type = Enum("Decor_Type", ["bookcase", "counter", "bed", "painting", "sofa"])


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
        self.text = None

        match self.obj_type:
            case Obj_Type.wall:
                animation_steps = 2
                self.collide = False
                self.interact = False

            case Obj_Type.door:
                filepath = Path("../res/doors.png")
                animation_steps = 8
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
                        self.text = Text(0, "Water Bottle")
                        ind = 0

                    case Pickup_Type.rat_poison:
                        self.text = Text(0, "Rat Poison")
                        ind = 2

                    case Pickup_Type.banana:
                        self.text = Text(0, "Priceless Banana Art")
                        ind = 4

                    case Pickup_Type.screwdriver:
                        self.text = Text(0, "screwdriver")
                        ind = 6

                    case Pickup_Type.will:
                        self.text = Text(0, "will, Press E to interact")
                        ind = 8

            case Obj_Type.interact:
                filepath = Path("../res/interact.png")
                animation_steps = 14
                self.collide = False
                self.interact = True

                # If the correct pickup has been used
                self.active = False

                match self.interact_type:

                    case Interact_Type.stove:
                        self.text = Text(0, "turn on gas - requires none")
                        self.collide = True
                        ind = 0
                        self.pickup_type = []

                    case Interact_Type.whiskey:
                        self.text = Text(0, "poison whiskey - requires: rat poison")
                        ind = 2
                        self.pickup_type = [Pickup_Type.rat_poison]

                    case Interact_Type.wine:
                        self.text = Text(0, "poison wine - requires: rat poison")
                        ind = 4
                        self.pickup_type = [Pickup_Type.rat_poison]

                    case Interact_Type.gramophone:
                        self.text = Text(0, "overload gramophone - requires: water bottle or screwdriver")
                        self.collide = True
                        ind = 6
                        self.pickup_type = [Pickup_Type.water_bottle, Pickup_Type.screwdriver]

                    case Interact_Type.armour:
                        self.text = Text(0, "loosen axe - requires: screwdriver")
                        self.collide = True
                        ind = 8
                        self.pickup_type = [Pickup_Type.screwdriver]

                    case Interact_Type.telephone:

                        self.text = Text(0, "electrify phone - requires: water bottle")
                        self.collide = True
                        ind = 10
                        self.pickup_type = [Pickup_Type.water_bottle]

                    case Interact_Type.bookshelf:
                        self.text = Text(0, "destabilise bookshelf - requires: screwdriver")
                        self.collide = True
                        animation_steps = 4
                        filepath = Path("../res/bookcase.png")
                        ind = 2
                        self.pickup_type = [Pickup_Type.screwdriver]

                    case Interact_Type.window:
                        self.text = Text(0, "place banana peel next to open window - requires: banana")
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

                    case Decor_Type.bed:
                        filepath = Path("../res/bed.png")
                        animation_steps = 2

                    case Decor_Type.painting:
                        filepath = Path("../res/paintings.png")
                        animation_steps = 2

                    case Decor_Type.sofa:
                        filepath = Path("../res/sofa.png")
                        animation_steps = 1

            case Obj_Type.other:
                animation_steps = 1
                self.collide = True
                self.interact = False
        
        
        x_pos = 0
        y_pos = 0
        super().__init__(x_pos, y_pos, filepath, animation_steps, ind)
