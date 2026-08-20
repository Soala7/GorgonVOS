"""
Gorgon OS (VOS)

Dock
"""

from __future__ import annotations

import sys
from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.ui.widgets.widget import Widget
from desktop.ui.core.event import MouseButton, MousePressEvent, MouseReleaseEvent
from desktop.assests.icon_manager import IconManager

class Dock(Widget):

    ICON_SIZE = 45
    SLOT_SIZE = 50
    MAX_ICONS = 7
    SPACING = 18
    BOTTOM_MARGIN = 35

    def __init__(self) -> None:
        self.launcher = None

        self.browser = None
        self.explorer = None
        self.terminal = None
        self.text_editor = None
        self.music = None
        self.settings = None
        self.visible = False
        self.animating = False

        self.hide_delay = 0.8
        self.hide_timer = 0.0

        self.hidden_offset = 70
        self.slide_offset = self.hidden_offset

        self.animation_speed = 550

        super().__init__("Dock")

        self.mouse_pos = (0, 0)

        self.icons = [

            IconManager.get("launcher/logo", self.ICON_SIZE),
            IconManager.get("launcher/browser", self.ICON_SIZE),
            IconManager.get("launcher/explorer", self.ICON_SIZE),
            IconManager.get("launcher/music", self.ICON_SIZE),
            IconManager.get("launcher/note", self.ICON_SIZE),
            IconManager.get("launcher/terminal", self.ICON_SIZE),
            IconManager.get("launcher/settings", self.ICON_SIZE),

        ]

    def update(self, dt):

        self.mouse_pos = pygame.mouse.get_pos()

        screen_height = pygame.display.get_surface().get_height()

        activation_zone = screen_height - 120

        if self.mouse_pos[1] >= activation_zone:

            self.visible = True
            self.animating = True
            self.hide_timer = self.hide_delay

        elif self.visible:

            self.hide_timer -= dt

            if self.hide_timer <= 0:

                self.visible = False
                self.animating = True

        target = 0 if self.visible else self.hidden_offset

        if self.slide_offset < target:

            self.slide_offset = min(
                self.slide_offset + self.animation_speed * dt,
                target,
            )

        elif self.slide_offset > target:

            self.slide_offset = max(
                self.slide_offset - self.animation_speed * dt,
                target,
            )

        if self.slide_offset == target:

            self.animating = False

    def _toggle_app_window(self, app) -> None:
        window = getattr(app, "window", None)
        window_manager = getattr(app, "window_manager", None)

        if window is None or window_manager is None:
            return

        if window in window_manager.windows and not window.closed and not window.minimized:
            window.minimize()
            if window_manager.active_window is window:
                window_manager.active_window = None
            return

        if window in window_manager.windows and window.minimized:
            window.restore()
        app.open()

    def handle_event(self, event):

        if not self.visible:
            return

        if self.animating:
            return

        if not isinstance(event, MousePressEvent):
            return

        if event.button != MouseButton.LEFT:
            return

        width = pygame.display.get_surface().get_width()
        height = pygame.display.get_surface().get_height()

        total_width = (
            self.MAX_ICONS * self.SLOT_SIZE
            + (self.MAX_ICONS - 1) * self.SPACING
        )

        start_x = (width - total_width) // 2

        y = (
            height
            - self.BOTTOM_MARGIN
            - self.SLOT_SIZE
        )

        for i in range(self.MAX_ICONS):

            x = start_x + i * (self.SLOT_SIZE + self.SPACING)

            if (
                x <= event.x <= x + self.SLOT_SIZE
                and
                y <= event.y <= y + self.SLOT_SIZE
            ):

                if i == 0:
                    if self.launcher:
                        self.launcher.toggle()
                        print("[Dock] Launcher")

                elif i == 1:
                    if self.browser:
                        self._toggle_app_window(self.browser)
                        print("[Dock] Browser")

                elif i == 2:
                    if self.explorer:
                        self._toggle_app_window(self.explorer)
                        print("[Dock] Explorer")

                elif i == 3:
                    if self.music:
                        self._toggle_app_window(self.music)
                    print("[Dock] Music")

                elif i == 4:
                    if self.text_editor:
                        self._toggle_app_window(self.text_editor)

                    print("[Dock] Notes")

                elif i == 5:
                    if self.terminal:
                        self._toggle_app_window(self.terminal)
                        print("[Dock] Terminal")

                elif i == 6:
                    if self.settings:
                        self._toggle_app_window(self.settings)
                    print("[Dock] Settings")

                break
    def draw(self, renderer) -> None:
        if not self.visible and not self.animating:
            return

        surface = renderer.surface

        width = surface.get_width()
        height = surface.get_height()

        total_width = (
            self.MAX_ICONS * self.SLOT_SIZE
            + (self.MAX_ICONS - 1) * self.SPACING
        )

        start_x = (width - total_width) // 2

        y = (
            height
            - self.BOTTOM_MARGIN
            - self.SLOT_SIZE
            + self.slide_offset
        )

        for i in range(self.MAX_ICONS):

            x = start_x + i * (
                self.SLOT_SIZE + self.SPACING
            )

            shadow = pygame.Surface(
                (self.SLOT_SIZE, self.SLOT_SIZE),
                pygame.SRCALPHA,
            )

            pygame.draw.circle(
                shadow,
                (0, 0, 0, 55),
                (
                    self.SLOT_SIZE // 2,
                    self.SLOT_SIZE // 2,
                ),
                self.SLOT_SIZE // 2,
            )

            surface.blit(shadow, (x, y))

            mouse_x, mouse_y = self.mouse_pos

            hovered = (
                self.visible
                and not self.animating
                and x <= mouse_x <= x + self.SLOT_SIZE
                and y <= mouse_y <= y + self.SLOT_SIZE
            )

            color = (
                (72, 72, 78)
                if hovered
                else
                (52, 52, 58)
            )

            pygame.draw.circle(
                surface,
                (95, 95, 105),
                (
                    x + self.SLOT_SIZE // 2,
                    y + self.SLOT_SIZE // 2,
                ),
                self.SLOT_SIZE // 2,
                1,
            )

            icon = self.icons[i]

            if icon is not None:

                draw_icon = icon

                if hovered:

                    draw_icon = pygame.transform.smoothscale(
                        icon,
                        (
                            int(self.ICON_SIZE * 1.08),
                            int(self.ICON_SIZE * 1.08),
                        ),
                    )

                surface.blit(
                    draw_icon,
                    (
                        x + (self.SLOT_SIZE - draw_icon.get_width()) // 2,
                        y + (self.SLOT_SIZE - draw_icon.get_height()) // 2,
                    ),
                )
