import pygame

from desktop.shell.wallpaper import Wallpaper
from desktop.renderer.pygame_renderer import PygameRenderer

def main():

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))

    renderer = PygameRenderer(screen)

    wallpaper = Wallpaper()

    renderer.clear((0, 0, 0))

    wallpaper.draw(
        renderer,
        1280,
        720,
    )

    pygame.display.flip()

    pygame.time.wait(1000)

    pygame.quit()

    print("Wallpaper render test passed.")

if __name__ == "__main__":

    main()
