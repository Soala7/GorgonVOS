"""
Gorgon OS (VOS)

Image widget.
"""

from __future__ import annotations

from desktop.ui.widgets.widget import Widget

class Image(Widget):
    """
    Displays an image.
    """

    def __init__(
        self,
        image=None,
        name: str = "Image",
    ) -> None:

        super().__init__(name)

        self.image = image

        self.keep_aspect = True

    def set_image(self, image) -> None:
        self.image = image

    def clear_image(self) -> None:
        self.image = None

    def on_draw(self, renderer) -> None:

        if self.image is None:
            return

        renderer.draw_image(
            image=self.image,
            bounds=self.transform.bounds,
            keep_aspect=self.keep_aspect,
        )
