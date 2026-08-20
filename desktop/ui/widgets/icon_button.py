"""
Gorgon OS (VOS)

Icon Button
"""

from __future__ import annotations

import pygame

from desktop.ui.widgets.widget import Widget

class IconButton(Widget):

    def __init__(
        self,
        name: str,
        icon,
        x: int = 0,
        y: int = 0,
        size: int = 70,
    ) -> None:

        super().__init__(name)

        self.icon = icon

        self.x = x
        self.y = y

        self.size = size

        self.hovered = False

        self.pressed = False

        self.tooltip = name

    def contains(self, mouse_pos):

        mx, my = mouse_pos

        return (
            self.x <= mx <= self.x + self.size
            and
            self.y <= my <= self.y + self.size
        )

    def update(self, dt):

        self.hovered = self.contains(
            pygame.mouse.get_pos()
        )

    def draw(self, renderer):

        surface = renderer.surface

        shadow = pygame.Surface(
            (self.size, self.size),
            pygame.SRCALPHA,
        )

        pygame.draw.circle(
            shadow,
            (0, 0, 0, 55),
            (
                self.size // 2,
                self.size // 2,
            ),
            self.size // 2,
        )

        surface.blit(
            shadow,
            (
                self.x,
                self.y,
            ),
        )

        color = (
            (72, 72, 80)
            if self.hovered
            else
            (52, 52, 58)
        )

        pygame.draw.circle(
            surface,
            color,
            (
                self.x + self.size // 2,
                self.y + self.size // 2,
            ),
            self.size // 2,
        )

        pygame.draw.circle(
            surface,
            (95, 95, 105),
            (
                self.x + self.size // 2,
                self.y + self.size // 2,
            ),
            self.size // 2,
            1,
        )

        if self.icon:

            surface.blit(
                self.icon,
                (
                    self.x + (self.size - self.icon.get_width()) // 2,
                    self.y + (self.size - self.icon.get_height()) // 2,
                ),
            )
