from __future__ import annotations

from apps.browser.browser_window import BrowserWindow


class Browser:
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.window = BrowserWindow(window_manager)

    def open(self):
        if self.window.closed:
            self.window = BrowserWindow(self.window_manager)
        self.window.open()

    def close(self):
        if self.window_manager:
            self.window_manager.close_window(self.window)
