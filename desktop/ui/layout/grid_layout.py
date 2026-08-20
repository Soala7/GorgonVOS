"""
Gorgon OS (VOS)

Grid Layout
"""

from __future__ import annotations

from desktop.ui.layout.base_layout import BaseLayout
from desktop.ui.core.container import Container

class GridLayout(BaseLayout):
    """
    Arranges children in a grid.
    """

    def __init__(
        self,
        columns: int = 1,
        spacing: int = 0,
        margin: int = 0,
    ) -> None:

        super().__init__(spacing, margin)

        self.columns = max(1, columns)

    def apply(self, container: Container) -> None:

        x = self.margin
        y = self.margin

        column = 0
        row_height = 0

        for child in container.children:

            child.transform.move_to(x, y)

            row_height = max(
                row_height,
                child.transform.size.height,
            )

            column += 1

            if column >= self.columns:

                column = 0

                x = self.margin

                y += row_height + self.spacing

                row_height = 0

            else:

                x += (
                    child.transform.size.width
                    + self.spacing
                )
