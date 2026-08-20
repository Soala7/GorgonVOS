"""
Gorgon OS (VOS)

Title Bar
"""

from __future__ import annotations

from desktop.ui.widgets.panel import Panel
from desktop.ui.widgets.label import Label

class TitleBar(Panel):
    """
    Displays the window title.
    """

    HEIGHT = 32

    def __init__(
        self,
        title: str = "Window",
    ) -> None:

        super().__init__("TitleBar")

        self.transform.resize(0, self.HEIGHT)

        self.title_label = Label(title)

        self.add_child(self.title_label)

    @property
    def title(self) -> str:
        return self.title_label.text

    @title.setter
    def title(self, value: str) -> None:
        self.title_label.set_text(value)
