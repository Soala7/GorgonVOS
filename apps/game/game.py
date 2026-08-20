from __future__ import annotations

from apps.game.game_window import GameWindow


class Game:
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.window = GameWindow(window_manager)

    def open(self):
        if self.window.closed:
            self.window = GameWindow(self.window_manager)
        self.window.restore()
        if self.window not in self.window_manager.windows:
            self.window_manager.add_window(self.window)
        else:
            self.window_manager.focus_window(self.window)

    def close(self):
        if self.window_manager:
            self.window_manager.close_window(self.window)
