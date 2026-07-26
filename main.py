"""
Gorgon OS (VOS)

Main Entry Point
"""

from __future__ import annotations

import pygame

from desktop.boot.boot_manager import BootManager
from desktop.renderer.pygame_renderer import PygameRenderer

from filesystem.filesystem import FileSystem
from bridge.vos_api import vos_api


WIDTH = 1600
HEIGHT = 900
FPS = 60


def main() -> None:

    pygame.init()
    pygame.mouse.set_visible(False)

    pygame.display.set_caption("Gorgon VOS")

    screen = pygame.display.set_mode(
        (
            WIDTH,
            HEIGHT,
        ),
        pygame.RESIZABLE,
    )


    # -----------------------------
    # Initialize VOS core services
    # -----------------------------

    filesystem = FileSystem()

    vos_api.register_filesystem(
        filesystem
    )


    # -----------------------------
    # Start graphics system
    # -----------------------------

    clock = pygame.time.Clock()

    renderer = PygameRenderer(screen)


    boot = BootManager()


    running = True


    while running:

        dt = clock.tick(FPS) / 1000


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            else:

                boot.handle_event(event)


        boot.update(dt)


        renderer.begin_frame()

        renderer.clear(
            (18,18,18)
        )

        boot.draw(renderer)

        renderer.end_frame()


    pygame.quit()


if __name__ == "__main__":

    main()