"""
Gorgon OS (VOS)

Main Entry Point
"""

from __future__ import annotations

import pygame

from desktop.boot.boot_manager import BootManager
from desktop.renderer.pygame_renderer import PygameRenderer
from desktop.ui.window.window_manager import WindowManager
from apps.explorer.explorer_window import ExplorerWindow
from kernel.kernel import Kernel

WIDTH = 1600
HEIGHT = 900
FPS = 60


def main() -> None:

    # -----------------------------
    # Initialize Pygame FIRST
    # -----------------------------
    pygame.init()

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Gorgon VOS")

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT),
        pygame.RESIZABLE,
    )

    # -----------------------------
    # Window Manager
    # -----------------------------
    window_manager = WindowManager()

    explorer = ExplorerWindow()
    window_manager.add_window(explorer)

    # -----------------------------
    # Start VOS Kernel
    # -----------------------------
    kernel = Kernel()
    kernel.boot()

    # -----------------------------
    # Graphics
    # -----------------------------
    clock = pygame.time.Clock()
    renderer = PygameRenderer(screen)

    # -----------------------------
    # Boot Manager
    # -----------------------------
    boot = BootManager(kernel)

    running = True

    while running:

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                kernel.shutdown()
                running = False

            else:
                boot.handle_event(event)

        boot.update(dt)

        renderer.begin_frame()
        renderer.clear((18, 18, 18))

        boot.draw(renderer)

        renderer.end_frame()

    pygame.quit()


if __name__ == "__main__":
    main()