"""
Gorgon OS (VOS)

Vertical Layout
"""

from __future__ import annotations

from desktop.ui.layout.base_layout import BaseLayout
from desktop.ui.core.container import Container

class VerticalLayout(BaseLayout):
    """
    Arranges children vertically.
    """

    def apply(self, container: Container) -> None:

        y = self.margin

        for child in container.children:

            child.transform.move_to(
                self.margin,
                y,
            )

            y += (
                child.transform.size.height
                + self.spacing
            )
