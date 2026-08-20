"""
Gorgon OS (VOS)

Start Menu
"""

from __future__ import annotations

from desktop.ui.widgets.panel import Panel
from desktop.ui.layout.vertical_layout import VerticalLayout

class StartMenu(Panel):
    """
    Desktop Start Menu.
    """

    def __init__(self) -> None:

        super().__init__("StartMenu")

        self.visible = False

        self.layout = VerticalLayout(
            spacing=4,
            margin=8,
        )

    def open(self) -> None:

        self.visible = True

    def close(self) -> None:

        self.visible = False

    def toggle(self) -> None:

        self.visible = not self.visible

    def add_item(self, item) -> None:

        self.add_child(item)

        self.layout.apply(self)
