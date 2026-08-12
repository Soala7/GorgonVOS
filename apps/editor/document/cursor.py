"""
Gorgon OS (VOS)

Editor Cursor
Handles cursor position and navigation.
"""

from __future__ import annotations


class EditorCursor:
    """
    Represents the cursor position inside an EditorDocument.

    The cursor does not modify the document.
    It only tracks where editing is taking place.
    """

    def __init__(
        self,
        row: int = 0,
        col: int = 0,
    ) -> None:

        self.row = row
        self.col = col

        # Used by vertical movement so the cursor
        # can remember its preferred horizontal position.
        self.preferred_col = col

    # --------------------------------------------------
    # Position
    # --------------------------------------------------

    def set_position(
        self,
        row: int,
        col: int,
        lines: list[str],
    ) -> None:

        self.row = max(
            0,
            min(row, len(lines) - 1),
        )

        self.col = max(
            0,
            min(col, len(lines[self.row])),
        )

        self.preferred_col = self.col

    def reset(self) -> None:

        self.row = 0
        self.col = 0
        self.preferred_col = 0

    # --------------------------------------------------
    # Horizontal Movement
    # --------------------------------------------------

    def move_left(
        self,
        lines: list[str],
    ) -> None:

        if self.col > 0:

            self.col -= 1

        elif self.row > 0:

            self.row -= 1
            self.col = len(lines[self.row])

        self.preferred_col = self.col

    def move_right(
        self,
        lines: list[str],
    ) -> None:

        current_line = lines[self.row]

        if self.col < len(current_line):

            self.col += 1

        elif self.row < len(lines) - 1:

            self.row += 1
            self.col = 0

        self.preferred_col = self.col

    # --------------------------------------------------
    # Vertical Movement
    # --------------------------------------------------

    def move_up(
        self,
        lines: list[str],
    ) -> None:

        if self.row <= 0:
            return

        self.preferred_col = max(
            self.preferred_col,
            self.col,
        )

        self.row -= 1

        self.col = min(
            self.preferred_col,
            len(lines[self.row]),
        )

    def move_down(
        self,
        lines: list[str],
    ) -> None:

        if self.row >= len(lines) - 1:
            return

        self.preferred_col = max(
            self.preferred_col,
            self.col,
        )

        self.row += 1

        self.col = min(
            self.preferred_col,
            len(lines[self.row]),
        )

    # --------------------------------------------------
    # Line Movement
    # --------------------------------------------------

    def move_home(
        self,
        lines: list[str],
    ) -> None:

        self.col = 0
        self.preferred_col = 0

    def move_end(
        self,
        lines: list[str],
    ) -> None:

        self.col = len(lines[self.row])
        self.preferred_col = self.col

    # --------------------------------------------------
    # Position Updates After Editing
    # --------------------------------------------------

    def after_insert(
        self,
        amount: int,
    ) -> None:

        self.col += amount
        self.preferred_col = self.col

    def after_newline(
        self,
        row: int,
        col: int,
    ) -> None:

        self.row = row
        self.col = col
        self.preferred_col = col

    def after_delete(
        self,
        row: int,
        col: int,
    ) -> None:

        self.row = row
        self.col = col
        self.preferred_col = col