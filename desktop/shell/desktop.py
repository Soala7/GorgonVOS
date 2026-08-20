"""
Gorgon OS (VOS)

Desktop
"""

from __future__ import annotations
from desktop.ui.widgets.panel import Panel
from desktop.shell.wallpaper import Wallpaper
from desktop.ui.window.window_manager import WindowManager
from desktop.shell.compositor import Compositor
from desktop.shell.start_menu import StartMenu
from desktop.shell.status_bar import StatusBar
from desktop.shell.desktop_icons import DesktopIcons
from desktop.shell.dock import Dock
from desktop.shell.launcher import Launcher
from desktop.shell.notification_center import NotificationCenter
from desktop.ui.core.event import MousePressEvent
import pygame

class Desktop(Panel):
    """
    Root desktop container.
    """

    def __init__(self):

        super().__init__("Desktop")

        self.desktop_icons = DesktopIcons()
        self.dock = Dock()
        self.launcher = Launcher()
        self.notification_center = NotificationCenter()
        self.window_manager = WindowManager()
        self.status_bar = StatusBar()

        self.wallpaper = Wallpaper()
        wallpaper = pygame.image.load(
                "assets/wallpapers/default.png"
            ).convert()

        self.wallpaper.set_image(wallpaper)

        self.compositor = Compositor(self)

        self.start_menu = StartMenu()


    def set_wallpaper(self, image) -> None:

        self.wallpaper.set_image(image)

    def set_wallpaper_path(self, path: str) -> None:
        self.wallpaper.load(path)

    def add_window(self, window) -> None:

        self.window_manager.add_window(window)

    def remove_window(self, window) -> None:

        self.window_manager.remove_window(window)

    def update(self, dt: float) -> None:

        self.desktop_icons.update(dt)
        self.dock.update(dt)

        if self.launcher:
            self.launcher.update(dt)

        self.notification_center.update(dt)

        self.window_manager.update(dt)

    def draw(self, renderer) -> None:

        self.wallpaper.draw(
            renderer,
            renderer.surface.get_width(),
            renderer.surface.get_height(),
        )

        self.desktop_icons.draw(renderer)

        self.window_manager.draw(renderer)

        self.dock.draw(renderer)

        self.status_bar.draw(renderer)

        if self.launcher:
            self.launcher.draw(renderer)

        self.notification_center.draw(renderer)

    def handle_event(self, event) -> None:
        if isinstance(event, MousePressEvent):

            if self.launcher and self.launcher.visible:

                if self.launcher.handle_click((event.x, event.y)):
                    event.handled = True
                    return

        self.notification_center.handle_event(event)

        if event.handled:
            return

        if self.launcher:
            self.launcher.handle_event(event)

        if event.handled:
            return

        self.status_bar.handle_event(event)

        if event.handled:
            return

        self.window_manager.handle_event(event)

        if event.handled:
            return

        self.dock.handle_event(event)

        if event.handled:
            return

        self.desktop_icons.handle_event(event)
