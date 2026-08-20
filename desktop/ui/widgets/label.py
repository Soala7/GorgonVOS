"""
Gorgon OS (VOS)

Label widget.
"""

from __future__ import annotations

from desktop.ui.widgets.widget import Widget

class Label(Widget):
    """
    Displays text.
    """

    def __init__(
        self,
        text: str = "",
        name: str = "Label",
    ) -> None:

        super().__init__(name)

        self.text = text

        self.font = None

        self.color = (255, 255, 255)

        self.align = "left"

    def set_text(self, text: str) -> None:
        self.text = text

    def set_font(self, font) -> None:
        self.font = font

    def set_color(self, color) -> None:
        self.color = color

    def set_alignment(self, alignment: str) -> None:
        self.align = alignment

    def on_draw(self, renderer) -> None:

        if self.font is None:
            return

        renderer.draw_text(
            text=self.text,
            font=self.font,
            color=self.color,
            position=self.transform.position,
            align=self.align,
        )
