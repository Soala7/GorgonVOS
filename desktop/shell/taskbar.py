"""
Gorgon OS (VOS)

Floating Dock
"""

from __future__ import annotations

import pygame

class Taskbar:

    HEIGHT = 72
    RADIUS = 24

    def __init__(self):

        self.apps = [
            "Explorer",
            "Browser",
            "Terminal",
            "Settings",
            "Store",
        ]

    def draw(self, renderer):

        surface = renderer.surface

        width = surface.get_width()
        height = surface.get_height()

        dock_width = 540
        dock_height = 72

        x = (width - dock_width) // 2
        y = height - 95

        pygame.draw.rect(
            surface,
            (36, 40, 50),
            (
                x,
                y,
                dock_width,
                dock_height,
            ),
            border_radius=self.RADIUS,
        )

        start_x = x + 42
        start_y = y + dock_height // 2

        pygame.draw.circle(
            surface,
            (60, 125, 255),
            (
                start_x,
                start_y,
            ),
            18,
        )

        icon_x = start_x + 55

        for _ in self.apps:

            pygame.draw.circle(
                surface,
                (215, 215, 220),
                (
                    icon_x,
                    start_y,
                ),
                15,
            )

            pygame.draw.circle(
                surface,
                (90, 170, 255),
                (
                    icon_x,
                    start_y + 24,
                ),
                3,
            )

            icon_x += 52

        font = pygame.font.SysFont(
            "arial",
            18,
        )
