"""
Gorgon OS (VOS)

Drawing Helpers
"""

from __future__ import annotations

import pygame

def rounded_rect(
    surface: pygame.Surface,
    color,
    rect,
    radius: int = 12,
) -> None:
    """
    Draw a rounded rectangle.
    """

    pygame.draw.rect(
        surface,
        color,
        pygame.Rect(
            rect.x,
            rect.y,
            rect.width,
            rect.height,
        ),
        border_radius=radius,
    )

def outline(
    surface: pygame.Surface,
    color,
    rect,
    width: int = 1,
    radius: int = 12,
) -> None:
    """
    Draw a rounded outline.
    """

    pygame.draw.rect(
        surface,
        color,
        pygame.Rect(
            rect.x,
            rect.y,
            rect.width,
            rect.height,
        ),
        width,
        border_radius=radius,
    )

def circle(
    surface: pygame.Surface,
    color,
    x: int,
    y: int,
    radius: int,
) -> None:

    pygame.draw.circle(
        surface,
        color,
        (x, y),
        radius,
    )

def line(
    surface: pygame.Surface,
    color,
    start,
    end,
    width: int = 1,
) -> None:

    pygame.draw.line(
        surface,
        color,
        start,
        end,
        width,
    )

def image(
    surface: pygame.Surface,
    img: pygame.Surface,
    rect,
) -> None:

    surface.blit(
        img,
        (
            rect.x,
            rect.y,
        ),
    )
