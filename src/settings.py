from enum import Enum

class ivec2:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

class fvec2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class Settings:
    def __init__(self) -> None:
        self.running = True
        self.restart = True



# u = up, d = down, l = left, r = right
Direction = Enum('Direction', ['ul', 'dl', 'dr', 'ur'])

WIDTH = 900
HEIGHT = 700

TILE_W = 128
TILE_H = 64

ISO_RATIO = TILE_W/TILE_H

_BASE_SPEED = 70
SPEED =  fvec2(_BASE_SPEED*ISO_RATIO, _BASE_SPEED)

class GameVars:
    ##this is where we can keep all the information for the game, current score, current room to show ect.
    ###if we create it twice it should be easy to reload
    def __init__(self) -> None:
        
    ###the rooms that will be in the game are, study, hallway, dinning room, kitchen, bedroom1, bedroom2, library, lounge
        self.current_room: int = 0
        self.rooms = []
        self.chars = []
        ###needs to go on the screen somewhere
        self.score = 0

        # Fail state
        self.caught =  False

        # Win state
        self.win = False

        self.time = 0
        self.dt = 0

    ###to work out what screen we're on, 
    def _check_win_state(self) -> bool:
        win = False
        for c in self.chars:
            if c.alive:
                return False
        return True
    
    def set_win_state(self):
        if self.caught == False:
            self.win = self._check_win_state()
        




