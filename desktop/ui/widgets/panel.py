"""
Gorgon OS (VOS)

Panel widget.
"""

from __future__ import annotations

from desktop.ui.core.container import Container


class Panel(Container):
    def __init__(self, name: str = "Panel") -> None:
        super().__init__(name)

        self.background_color = None

        self.border_color = None

        self.border_width = 0

    def set_background(self, color) -> None:
        self.background_color = color

    def set_border(
        self,
        color,
        width: int = 1,
    ) -> None:

        self.border_color = color
        self.border_width = width

    def clear_border(self) -> None:

        self.border_color = None
        self.border_width = 0

    def on_draw(self, renderer) -> None:

        if self.background_color is not None:

            renderer.draw_rect(
                self.transform.bounds,
                self.background_color,
            )

        if (
            self.border_color is not None
            and self.border_width > 0
        ):

            renderer.draw_rect_outline(
                self.transform.bounds,
                self.border_color,
                self.border_width,
            )