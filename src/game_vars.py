from text import Text_Event

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

        self.text_events = Text_Event()

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
        