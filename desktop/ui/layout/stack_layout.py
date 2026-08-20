"""
Gorgon OS (VOS)

Stack Layout
"""

from __future__ import annotations

from desktop.ui.layout.base_layout import BaseLayout
from desktop.ui.core.container import Container

class StackLayout(BaseLayout):
    """
    Places every child in the same position.
    Useful for pages, overlays and dialogs.
    """

    def apply(self, container: Container) -> None:

        for child in container.children:

            child.transform.move_to(
                self.margin,
                self.margin,
            )
