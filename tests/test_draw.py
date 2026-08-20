import pygame
from desktop.renderer.draw import (
    rounded_rect,
    outline,
    circle,
    line,
)

class Rect:

    def __init__(self):

        self.x = 50
        self.y = 50
        self.width = 200
        self.height = 100

def main():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    r = Rect()

    rounded_rect(
        screen,
        (255, 0, 0),
        r,
    )

    outline(
        screen,
        (255, 255, 255),
        r,
        2,
    )

    circle(
        screen,
        (0, 255, 0),
        400,
        200,
        40,
    )

    line(
        screen,
        (0, 0, 255),
        (50, 300),
        (500, 300),
        4,
    )

    pygame.display.flip()

    pygame.time.wait(500)

    pygame.quit()

    print("Draw helper tests passed.")

if __name__ == "__main__":
    main()
