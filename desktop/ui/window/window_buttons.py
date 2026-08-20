"""
Gorgon OS (VOS)

Window Buttons
"""

from __future__ import annotations

from desktop.ui.widgets.button import Button
from desktop.ui.widgets.panel import Panel
from desktop.ui.window.window import Window

class WindowButtons(Panel):
    """
    Minimize, Maximize and Close buttons.
    """

    def __init__(self, window: Window) -> None:

        super().__init__("WindowButtons")

        self.window = window

        self.minimize_button = Button("—")
        self.maximize_button = Button("□")
        self.close_button = Button("✕")

        self.minimize_button.on_click = self.window.minimize
        self.maximize_button.on_click = self.toggle_maximize
        self.close_button.on_click = self.window.close

        self.add_child(self.minimize_button)
        self.add_child(self.maximize_button)
        self.add_child(self.close_button)

    def toggle_maximize(self) -> None:

        if self.window.maximized:
            self.window.restore()
        else:
            self.window.maximize()
