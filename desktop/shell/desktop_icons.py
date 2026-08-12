"""
Gorgon OS (VOS)

Desktop Icons
"""

from __future__ import annotations

import pygame

from desktop.ui.widgets.panel import Panel
from desktop.ui.core.component import Component


class DesktopIcons(Panel):

    def __init__(self) -> None:

        super().__init__("DesktopIcons")

        self.icons = []

    def add_icon(self, icon: Component) -> None:

        self.add_child(icon)

    def remove_icon(self, icon: Component) -> None:

        self.remove_child(icon)

    def clear_icons(self) -> None:

        self.clear_children()

    def draw(self, renderer):

        surface = renderer.surface

        font = pygame.font.SysFont(
            "DejaVu Sans Mono",
            18,
        )

        for name, (x, y) in self.icons:

            # icon

            pygame.draw.circle(
                surface,
                (210, 210, 220),
                (
                    x,
                    y,
                ),
                24,
            )

            # text

            renderer.draw_text(
                name,
                font,
                (255, 255, 255),
                pygame.Vector2(
                    x - 25,
                    y + 35,
                ),
            )

        super().draw(renderer)