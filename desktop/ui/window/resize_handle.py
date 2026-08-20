"""
Gorgon OS (VOS)

Resize Handle
"""

from __future__ import annotations

from desktop.ui.widgets.widget import Widget

class ResizeHandle(Widget):
    """
    Window resize handle.
    """

    def __init__(
        self,
        edge: str = "bottom_right",
    ) -> None:

        super().__init__("ResizeHandle")

        self.edge = edge

        self.dragging = False

    def start_resize(self) -> None:

        self.dragging = True

    def stop_resize(self) -> None:

        self.dragging = False
