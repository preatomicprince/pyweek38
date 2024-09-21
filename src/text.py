import pygame
from typedefs import ivec2, WIDTH

class Text:
    def __init__(self, time, text: str, size: int = 32) -> None:
        font = pygame.font.Font("../res/Vogue.ttf", size)
        self.text = font.render(text, True, (255, 255, 255), (0, 0, 0))
        rect = self.text.get_rect()

        self.size = ivec2(rect.w, rect.h)

        self.time = time

    def draw(self, screen, x_pos, y_pos):
        rect  = pygame.Rect(x_pos, y_pos, self.size.x, self.size.y)
        screen.blit(self.text, rect)

class Text_Event:
    def __init__(self) -> None:
        self.events = []
        self.display_time = 5000

    def draw(self, screen) -> None:
        order = 0
        for e in self.events:
            e.draw(screen, order*e.size.y + 5, WIDTH - e.size.x - 5)

    def update(self, game_vars) -> None:
        for e in self.events:
            if game_vars.time > e.time + self.display_time:
                self.events.remove(e)

    def append(self, game_vars, text: str = ""):
        self.events.append(Text(game_vars.time, text))
