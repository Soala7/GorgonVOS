"""
Gorgon OS (VOS)

Boot Screen
"""

from __future__ import annotations

import time
import pygame


class BootScreen:

    def __init__(self,logo=None,duration: float = 3.0,) -> None:

        self.logo = logo

        self.duration = duration

        self.start_time = None

        self.finished = False

    # --------------------------------------------------
    # Boot
    # --------------------------------------------------

    def start(self) -> None:

        self.start_time = time.time()

        self.finished = False

    def update(self) -> None:

        if self.finished:
            return

        if self.start_time is None:
            return

        if time.time() - self.start_time >= self.duration:

            self.finished = True

    @property
    def progress(self) -> float:

        if self.start_time is None:
            return 0.0

        return min(
            (time.time() - self.start_time) / self.duration,
            1.0,
        )

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

    def draw(self,renderer) -> None:

        surface = renderer.surface

        width = surface.get_width()

        height = surface.get_height()

        renderer.clear((14, 14, 18))

        font = pygame.font.SysFont(
            "DejaVu Sans Mono",
            72,
            bold=True,
            italic = True
        )

        renderer.draw_text("GORGON",font,(255, 255, 255),pygame.Vector2(
                width // 2,
                height // 2 - 40),
            align="center",
        )

        pygame.draw.rect(
            surface,
            (60, 60, 60),
            (
                width // 2 - 200,
                height // 2 + 40,
                400,
                8,
            ),
            border_radius=8,
        )

        pygame.draw.rect(surface,(30, 180, 255),
            (
                width // 2 - 200,
                height // 2 + 40,
                int(400 * self.progress),
                8,
            ),
            border_radius=8,
        )