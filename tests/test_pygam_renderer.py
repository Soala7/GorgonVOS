import pygame

from desktop.renderer.pygame_renderer import PygameRenderer

def main():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    renderer = PygameRenderer(screen)

    renderer.begin_frame()

    renderer.clear((30, 30, 30))

    renderer.end_frame()

    pygame.quit()

    print("PygameRenderer tests passed.")

if __name__ == "__main__":
    main()
