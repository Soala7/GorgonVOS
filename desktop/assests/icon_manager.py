"""
Gorgon OS (VOS)

Universal Icon Manager
Supports SVG and PNG icons
"""

from __future__ import annotations

from pathlib import Path
from io import BytesIO

import pygame
import cairosvg

class IconLoadError(Exception):
    """Raised when an icon asset cannot be loaded."""

class IconManager:

    _cache: dict[tuple[str, int], pygame.Surface] = {}

    ROOT = Path("assets/icons")

    @classmethod
    def get(
        cls,
        icon: str,
        size: int = 60,
    ) -> pygame.Surface | None:

        if not pygame.get_init():
            try:
                pygame.init()
            except Exception:
                return None

        key = (icon, size)

        if key in cls._cache:
            return cls._cache[key]

        svg_path = cls.ROOT / f"{icon}.svg"
        png_path = cls.ROOT / f"{icon}.png"

        path = None
        file_type = None

        surface = None

        if svg_path.exists():

            try:

                png_bytes = cairosvg.svg2png(
                    url=str(svg_path),
                    output_width=size,
                    output_height=size,
                )

                surface = pygame.image.load(
                    BytesIO(png_bytes),
                    "icon.png",
                ).convert_alpha()

                print(f"[IconManager] Loaded SVG {icon}")

            except Exception:

                print(f"[IconManager] SVG failed ({icon}), trying PNG...")

        if surface is None and png_path.exists():

            try:

                surface = pygame.image.load(
                    str(png_path)
                ).convert_alpha()

                surface = pygame.transform.smoothscale(
                    surface,
                    (size, size)
                )

                print(f"[IconManager] Loaded PNG {icon}")

            except Exception as e:

                print(f"[IconManager] PNG failed ({icon}): {e}")

        if surface is None:

            print(f"[IconManager] Missing or invalid icon: {icon}")

            return None

        cls._cache[key] = surface

        return surface

        print(
            f"[IconManager] Loaded {file_type.upper()} {icon}"
        )

        return surface

    @classmethod
    def clear_cache(cls):

        cls._cache.clear()
