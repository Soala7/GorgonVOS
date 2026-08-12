"""
Gorgon OS (VOS)

Login Screen
"""

from __future__ import annotations

import pygame


class LoginScreen:

    def __init__(self) -> None:

        self.username = ""

        self.password = ""

        self.logged_in = False

        self.selected_user = None

    # --------------------------------------------------
    # User
    # --------------------------------------------------

    def select_user(self, username: str) -> None:

        self.selected_user = username

    # --------------------------------------------------
    # Login
    # --------------------------------------------------

    def login(self) -> bool:

        if self.selected_user is None:
            return False

        self.logged_in = True

        return True

    def logout(self) -> None:

        self.logged_in = False

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

    def draw(self, renderer) -> None:

        surface = renderer.surface

        width = surface.get_width()

        height = surface.get_height()

        renderer.clear((22, 24, 30))

        title_font = pygame.font.SysFont(
            "DejaVu Sans Mono",
            48,
            bold=True,
        )

        text_font = pygame.font.SysFont(
            "DejaVu Sans Mono",
            24,
        )

        # Avatar

        pygame.draw.circle(
            surface,
            (70, 120, 255),
            (
                width // 2,
                height // 2 - 90,
            ),
            45,
        )

        renderer.draw_text(
            "Guest",
            title_font,
            (255, 255, 255),
            pygame.Vector2(
                width // 2,
                height // 2,
            ),
            align="center",
        )

        renderer.draw_text(
            "Press ENTER to Login",
            text_font,
            (180, 180, 180),
            pygame.Vector2(
                width // 2,
                height // 2 + 60,
            ),
            align="center",
        )