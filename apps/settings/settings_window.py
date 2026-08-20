from __future__ import annotations

from pathlib import Path

import pygame

from desktop.ui.core.event import MouseButton, MousePressEvent
from desktop.ui.window.window import Window


class SettingsWindow(Window):
    def __init__(self, desktop):
        super().__init__(title="Settings", width=760, height=560, name="Settings")
        self.desktop = desktop
        self.transform.position.x = 220
        self.transform.position.y = 90
        self.font = pygame.font.SysFont("DejaVu Sans", 18, bold=True)
        self.small_font = pygame.font.SysFont("DejaVu Sans", 14)
        self.wallpapers = sorted(Path("assets/wallpapers").glob("*.png"))
        self.thumbnails = []
        for path in self.wallpapers:
            try:
                image = pygame.image.load(str(path)).convert()
                self.thumbnails.append((path, pygame.transform.smoothscale(image, (180, 105))))
            except pygame.error:
                continue

    def open(self):
        self.restore()
        if self not in self.desktop.window_manager.windows:
            self.desktop.window_manager.add_window(self)
        else:
            self.desktop.window_manager.focus_window(self)

    def handle_event(self, event):
        super().handle_event(event)
        if getattr(event, "handled", False) or not self.active or self.minimized:
            return
        if isinstance(event, MousePressEvent) and event.button == MouseButton.LEFT:
            x = int(self.transform.position.x)
            y = int(self.transform.position.y) + self.TITLEBAR_HEIGHT
            for index in range(len(self.thumbnails)):
                col = index % 3
                row = index // 3
                rect = pygame.Rect(x + 35 + col * 220, y + 100 + row * 145, 180, 105)
                if rect.collidepoint(event.x, event.y):
                    self.desktop.set_wallpaper_path(str(self.thumbnails[index][0]))
                    event.handled = True
                    return

    def draw(self, renderer):
        if self.minimized:
            return
        super().draw(renderer)
        surface = renderer.surface
        x = int(self.transform.position.x) + 2
        y = int(self.transform.position.y) + self.TITLEBAR_HEIGHT
        width = int(self.transform.size.width) - 4
        height = int(self.transform.size.height) - self.TITLEBAR_HEIGHT - 2
        pygame.draw.rect(surface, (18, 21, 38), (x, y, width, height))
        renderer.draw_text("Appearance", self.font, (240, 244, 255), pygame.Vector2(x + 35, y + 32))
        renderer.draw_text("Choose a wallpaper", self.small_font, (150, 165, 210), pygame.Vector2(x + 35, y + 62))
        for index, (path, image) in enumerate(self.thumbnails):
            col = index % 3
            row = index // 3
            rect = pygame.Rect(x + 35 + col * 220, y + 100 + row * 145, 180, 105)
            surface.blit(image, rect)
            pygame.draw.rect(surface, (95, 180, 255), rect, 2, border_radius=8)
            renderer.draw_text(path.stem, self.small_font, (230, 235, 250), pygame.Vector2(rect.x, rect.bottom + 8))
