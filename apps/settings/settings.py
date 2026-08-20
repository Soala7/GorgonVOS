from __future__ import annotations

from apps.settings.settings_window import SettingsWindow


class Settings:
    def __init__(self, desktop):
        self.desktop = desktop
        self.window = SettingsWindow(desktop)

    def open(self):
        if self.window.closed:
            self.window = SettingsWindow(self.desktop)
        self.window.open()

    def close(self):
        self.desktop.window_manager.close_window(self.window)
