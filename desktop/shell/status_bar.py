"""
Gorgon OS (VOS)

Desktop Status Bar
"""

from __future__ import annotations

import datetime
import pygame

from desktop.ui.widgets.widget import Widget
from desktop.assests.icon_manager import IconManager

class StatusBar(Widget):

    def __init__(self):

        super().__init__("StatusBar")

        self.notification = IconManager.get("launcher/notification", 24)
        self.wifi = IconManager.get("launcher/wifi", 24)
        self.volume = IconManager.get("launcher/volume", 24)

        self.battery = IconManager.get("launcher/battery", 44)

        self.time_font = pygame.font.SysFont(
            "arial",
            36,
            bold=True,
        )

        self.date_font = pygame.font.SysFont(
            "arial",
            18,
        )

    def draw_hover_icon_only(self, surface, icon, center, base_size, mouse_pos):
        """Helper to draw an icon inside our grouped panel that grows on hover."""
        if not icon:
            return

        distance = pygame.Vector2(center).distance_to(mouse_pos)
        hover = distance <= (base_size // 2) + 6

        draw_size = int(base_size * 1.16) if hover else base_size

        scaled_icon = pygame.transform.smoothscale(icon, (draw_size, draw_size))
        surface.blit(scaled_icon, (center[0] - draw_size // 2, center[1] - draw_size // 2))

    def draw(self, renderer):

        surface = renderer.surface

        width = surface.get_width()
        height = surface.get_height()
        mouse_pos = pygame.mouse.get_pos()

        start_x = width - 180
        y_pos = height - 900
        spacing = 50
        base_size = 35

        panel_rect = pygame.Rect(start_x - 12, y_pos - 8, 160, base_size + 16)

        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (0, 0, 0, 80), (0, 0, panel_rect.width, panel_rect.height), border_radius=14)
        pygame.draw.rect(panel_surface, (255, 255, 255, 200), (0, 0, panel_rect.width, panel_rect.height), 2, border_radius=14)
        surface.blit(panel_surface, panel_rect.topleft)

        icons = [
            self.notification,
            self.wifi,
            self.volume,
        ]

        curr_x = start_x
        for icon in icons:
            if icon:
                icon_center = (curr_x + base_size // 2, y_pos + base_size // 2)
                self.draw_hover_icon_only(surface, icon, icon_center, base_size, mouse_pos)

            curr_x += spacing

        y = height - 55
        battery_base_size = 44

        battery_x = width - 290
        battery_center = (battery_x + battery_base_size // 2, y + battery_base_size // 2)

        if self.battery:

            b_distance = pygame.Vector2(battery_center).distance_to(mouse_pos)
            b_hover = b_distance <= (battery_base_size // 2)
            b_draw_size = int(battery_base_size * 1.16) if b_hover else battery_base_size

            scaled_battery = pygame.transform.smoothscale(self.battery, (b_draw_size, b_draw_size))
            surface.blit(scaled_battery, (battery_center[0] - b_draw_size // 2, battery_center[1] - b_draw_size // 2))

        current_time = datetime.datetime.now().strftime("%H:%M")

        renderer.draw_text(
            current_time,
            self.time_font,
            (240, 240, 240),
            pygame.Vector2(
                width - 220,
                y + 5,
            ),
        )

        current_date = datetime.datetime.now().strftime("%d %b")

        renderer.draw_text(
            current_date,
            self.date_font,
            (180, 180, 180),
            pygame.Vector2(
                width - 110,
                y + 18,
            ),
        )
