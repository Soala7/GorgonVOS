"""
Gorgon OS (VOS)

Wallpaper Layer (Figma Style)
"""

from __future__ import annotations

import pygame

class Wallpaper:

    def __init__(self):
        self.image = None
        self.dim = 0

        self.load(
            "assets/wallpapers/default.png"
        )

    def set_image(self, image):

        self.image = image

    def load(self, path):

        self.image = pygame.image.load(path).convert()

    def draw(self, renderer, width: int, height: int):

        surface = renderer.surface

        if self.image is None:

            for y in range(height):

                ratio = y / height

                r = int(18 + ratio * 10)
                g = int(22 + ratio * 18)
                b = int(35 + ratio * 40)

                pygame.draw.line(
                    surface,
                    (r, g, b),
                    (0, y),
                    (width, y),
                )

        if self.image:

            renderer.draw_image(
                self.image,
                pygame.Rect(
                    0,
                    0,
                    width,
                    height,
                ),
                keep_aspect=False,
            )
        if self.dim > 0:

            overlay = pygame.Surface(
                (width, height),
                pygame.SRCALPHA,
            )

            overlay.fill(
                (0, 0, 0, self.dim)
            )

            renderer.surface.blit(
                overlay,
                (0, 0),
            )
