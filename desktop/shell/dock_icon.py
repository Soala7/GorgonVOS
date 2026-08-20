"""
Gorgon OS (VOS)

Dock Icon
"""

from __future__ import annotations

import pygame

class DockIcon:

    SIZE = 56

    def __init__(
        self,
        name: str,
        image=None,
    ):

        self.name = name

        self.image = image

        self.running = False

        self.notification = False

        self.position = pygame.Vector2()

    def draw(
        self,
        renderer,
    ):

        surface = renderer.surface

        x = int(self.position.x)
        y = int(self.position.y)

        shadow = pygame.Surface(
            (54, 18),
            pygame.SRCALPHA,
        )

        pygame.draw.ellipse(
            shadow,
            (40, 40, 40, 90),
            shadow.get_rect(),
        )

        surface.blit(
            shadow,
            (
                x - 27,
                y + 18,
            ),
        )

        pygame.draw.circle(
            surface,
            (215, 215, 220),
            (
                x,
                y,
            ),
            24,
        )

        if self.running:

            pygame.draw.circle(
                surface,
                (90, 170, 255),
                (
                    x,
                    y + 30,
                ),
                3,
            )
