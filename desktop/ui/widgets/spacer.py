"""
Gorgon OS (VOS)

Spacer widget.
"""

from __future__ import annotations

from desktop.ui.widgets.widget import Widget

class Spacer(Widget):
    """
    Invisible widget used to create empty space in layouts.
    """

    def __init__(
        self,
        width: int = 0,
        height: int = 0,
        name: str = "Spacer",
    ) -> None:

        super().__init__(name)

        self.transform.resize(width, height)

    def on_draw(self, renderer) -> None:

        pass
