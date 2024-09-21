import pygame
from typedefs import ivec2, WIDTH

class Text:
    def __init__(self, time, text: str,  display_time  = 1000, size: int = 16,) -> None:
        font = pygame.font.Font("../res/Vogue.ttf", size)
        self.text = font.render(text, True, (255, 255, 255), (0, 0, 0))
        rect = self.text.get_rect()

        self.size = ivec2(rect.w, rect.h)

        self.time = time
        self.display_time = display_time

    def draw(self, screen, x_pos, y_pos):
        rect  = pygame.Rect(x_pos, y_pos, self.size.x, self.size.y)
        screen.blit(self.text, rect)

class Text_Event:
    def __init__(self) -> None:
        self.events = []
        

    def draw(self, screen) -> None:
        order = 0
        max_displayed_events = 7
        
        for e in self.events:
            e.draw(screen, WIDTH - e.size.x - 10, order*(e.size.y + 10)+ 10)

            order += 1
            if order > max_displayed_events:
                break

    def update(self, game_vars) -> None:
        for e in self.events:
            if game_vars.time > e.time + e.display_time:
                self.events.remove(e)

    def append(self, game_vars, text: str = "", display_time = 10000):
        self.events.append(Text(game_vars.time, text, display_time))
