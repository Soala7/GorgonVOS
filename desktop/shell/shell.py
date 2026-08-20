"""
Gorgon OS (VOS)

Shell
"""

from __future__ import annotations

from desktop.renderer import renderer
from desktop.shell.desktop import Desktop
from apps.terminal.terminal import Terminal
from apps.explorer.explorer import Explorer
from apps.editor.editor import TextEditor
from apps.game.game import Game
from apps.music.music import Music
from apps.settings.settings import Settings
from apps.browser.browser import Browser

class Shell:
    """
    Main desktop shell.
    """

    def __init__(self, service_manager) -> None:

        self.lifecycle_action = None
        self.desktop = Desktop()

        self.terminal = Terminal(service_manager)

        self.explorer = Explorer(self.desktop.window_manager)

        self.text_editor = TextEditor(service_manager)

        self.game = Game(self.desktop.window_manager)
        self.music = Music(self.desktop.window_manager)
        self.settings = Settings(self.desktop)
        self.browser = Browser(self.desktop.window_manager)

        self.service_manager = service_manager

        self.terminal.window_manager = self.desktop.window_manager

        self.explorer.window_manager = self.desktop.window_manager

        self.text_editor.window_manager = self.desktop.window_manager

        self.desktop.launcher.app_launcher = self

        self.desktop.dock.launcher = self.desktop.launcher
        self.desktop.dock.terminal = self.terminal
        self.desktop.dock.explorer = self.explorer
        self.desktop.dock.text_editor = self.text_editor
        self.desktop.dock.music = self.music
        self.desktop.dock.settings = self.settings
        self.desktop.dock.browser = self.browser

    def launch_app(self, app_name: str) -> bool:
        apps = {
            "terminal": self.terminal,
            "explorer": self.explorer,
            "text_editor": self.text_editor,
            "game": self.game,
            "music": self.music,
            "settings": self.settings,
            "browser": self.browser,
        }
        app = apps.get(app_name)
        if app is None:
            print(f"[VOS] Unknown app: {app_name}")
            return False
        app.open()
        return True

    def power_action(self, action: str) -> bool:
        if action in {"shutdown", "restart", "logout"}:
            self.lifecycle_action = action
            return True
        if action == "sleep":
            self.desktop.wallpaper.dim = 160
            return True
        return False

    def consume_lifecycle_action(self):
        action = self.lifecycle_action
        self.lifecycle_action = None
        return action

    def update(self, dt: float) -> None:

        self.desktop.update(dt)

    def draw(self, renderer) -> None:

        self.desktop.draw(renderer)

    def handle_event(self, event) -> None:

        self.desktop.handle_event(event)
