"""
Gorgon OS (VOS)

Horizontal Layout
"""

from __future__ import annotations

from desktop.ui.layout.base_layout import BaseLayout
from desktop.ui.core.container import Container

class HorizontalLayout(BaseLayout):
    """
    Arranges children horizontally.
    """

    def apply(self, container: Container) -> None:

        x = self.margin

        for child in container.children:

            child.transform.move_to(
                x,
                self.margin,
            )

            x += (
                child.transform.size.width
                + self.spacing
            )
