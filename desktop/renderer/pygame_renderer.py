"""
Gorgon OS (VOS)

Pygame Renderer
"""

from __future__ import annotations

import pygame

from desktop.renderer.renderer import Renderer

class PygameRenderer(Renderer):

    def __init__(self, surface: pygame.Surface) -> None:

        self.surface = surface

    def begin_frame(self) -> None:
        pass

    def end_frame(self) -> None:
        pygame.display.flip()

    def clear(self, color) -> None:

        self.surface.fill(color)

    def draw_rect(self, rect, color) -> None:

        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(
                rect.x,
                rect.y,
                rect.width,
                rect.height,
            ),
        )

    def draw_rect_outline(
        self,
        rect,
        color,
        width=1,
    ) -> None:

        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(
                rect.x,
                rect.y,
                rect.width,
                rect.height,
            ),
            width,
        )

    def draw_text(
        self,
        text,
        font,
        color,
        position,
        align="left",
    ):

        rendered = font.render(
            text,
            True,
            color,
        )

        x = position.x
        y = position.y

        if align == "center":

            x -= rendered.get_width() // 2

        elif align == "right":

            x -= rendered.get_width()

        self.surface.blit(
            rendered,
            (x, y),
        )

    def draw_image(
        self,
        image,
        bounds,
        keep_aspect=True,
    ):

        if image is None:
            return

        if keep_aspect:

            img = pygame.transform.smoothscale(
                image,
                (
                    bounds.width,
                    bounds.height,
                ),
            )

        else:

            img = pygame.transform.scale(
                image,
                (
                    bounds.width,
                    bounds.height,
                ),
            )

        self.surface.blit(
            img,
            (
                bounds.x,
                bounds.y,
            ),
        )

    def draw_textbox(
        self,
        bounds,
        text,
        placeholder,
        focused,
    ):

        pygame.draw.rect(
            self.surface,
            (240, 240, 240),
            (
                bounds.x,
                bounds.y,
                bounds.width,
                bounds.height,
            ),
            border_radius=8,
        )
