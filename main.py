"""
Gorgon OS (VOS)
Main Entry Point
"""

from __future__ import annotations

import pygame

from boot.boot_manager import BootManager
from desktop.renderer.pygame_renderer import PygameRenderer
from desktop.ui.window.window_manager import WindowManager
from apps.explorer.explorer_window import ExplorerWindow
from kernel.kernel import Kernel

WIDTH = 1600
HEIGHT = 900
FPS = 60

def main() -> None:

    pygame.init()

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Gorgon VOS")

    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)

    window_manager = WindowManager()

    explorer = ExplorerWindow(window_manager)
    window_manager.add_window(explorer)

    kernel = Kernel()
    kernel.boot()

    clock = pygame.time.Clock()
    renderer = PygameRenderer(screen)

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

        lifecycle_action = boot.shell.consume_lifecycle_action()
        if lifecycle_action == "shutdown":
            kernel.shutdown()
            running = False
        elif lifecycle_action == "restart":
            boot.restart_session(boot_again=True)
        elif lifecycle_action == "logout":
            boot.restart_session()

        renderer.begin_frame()

        boot.draw(renderer)

        renderer.end_frame()

    pygame.quit()

if __name__ == "__main__":
    main()
