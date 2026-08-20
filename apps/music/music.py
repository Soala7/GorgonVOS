from __future__ import annotations

from apps.music.music_window import MusicWindow


class Music:
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.window = MusicWindow(window_manager)

    def open(self):
        if self.window.closed:
            self.window = MusicWindow(self.window_manager)
        self.window.open()

    def close(self):
        if self.window_manager:
            self.window_manager.close_window(self.window)
