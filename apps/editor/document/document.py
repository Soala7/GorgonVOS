"""
Gorgon OS (VOS)

Editor Document
Handles the text buffer independently from the GUI.
"""

from __future__ import annotations


class EditorDocument:
    """
    Represents the text currently being edited.

    This class does not know anything about Pygame,
    windows, rendering, or keyboard events.
    """

    def __init__(self, text: str = "") -> None:

        self.lines: list[str] = [""]
        self.dirty: bool = False

        self.set_text(text)

    # --------------------------------------------------
    # Document Content
    # --------------------------------------------------

    def set_text(self, text: str) -> None:
        """
        Replace the entire document with text.
        """

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        self.lines = text.split("\n")

        if not self.lines:
            self.lines = [""]

        self.dirty = False

    def get_text(self) -> str:
        """
        Return the complete document as a string.
        """

        return "\n".join(self.lines)

    def clear(self) -> None:
        """
        Clear the entire document.
        """

        self.lines = [""]
        self.dirty = True

    # --------------------------------------------------
    # Text Insertion
    # --------------------------------------------------

    def insert(
        self,
        row: int,
        col: int,
        text: str,
    ) -> int:
        """
        Insert text at row/column.

        Returns the new column position.
        """

        if not text:
            return col

        line = self.lines[row]

        self.lines[row] = (
            line[:col]
            + text
            + line[col:]
        )

        self.dirty = True

        return col + len(text)

    def insert_newline(
        self,
        row: int,
        col: int,
    ) -> tuple[int, int]:
        """
        Split the current line at the cursor.

        Returns:
            (new_row, new_col)
        """

        line = self.lines[row]

        left = line[:col]
        right = line[col:]

        self.lines[row] = left

        self.lines.insert(
            row + 1,
            right,
        )

        self.dirty = True

        return row + 1, 0

    # --------------------------------------------------
    # Deletion
    # --------------------------------------------------

    def delete_backward(
        self,
        row: int,
        col: int,
    ) -> tuple[int, int]:
        """
        Backspace operation.

        Returns the new cursor position.
        """

        # Delete character before cursor
        if col > 0:

            line = self.lines[row]

            self.lines[row] = (
                line[:col - 1]
                + line[col:]
            )

            self.dirty = True

            return row, col - 1

        # Join with previous line
        if row > 0:

            previous = self.lines[row - 1]
            current = self.lines.pop(row)

            new_col = len(previous)

            self.lines[row - 1] = (
                previous + current
            )

            self.dirty = True

            return row - 1, new_col

        # Beginning of document
        return row, col

    def delete_forward(
        self,
        row: int,
        col: int,
    ) -> tuple[int, int]:
        """
        Delete operation.

        Returns the new cursor position.
        """

        line = self.lines[row]

        # Delete character after cursor
        if col < len(line):

            self.lines[row] = (
                line[:col]
                + line[col + 1:]
            )

            self.dirty = True

            return row, col

        # Join next line
        if row < len(self.lines) - 1:

            self.lines[row] += (
                self.lines.pop(row + 1)
            )

            self.dirty = True

        return row, col

    # --------------------------------------------------
    # State
    # --------------------------------------------------

    def mark_saved(self) -> None:
        """
        Mark the current document as saved.
        """

        self.dirty = False

    def is_empty(self) -> bool:
        """
        Check whether the document contains no text.
        """

        return (
            len(self.lines) == 1
            and self.lines[0] == ""
        )

    def line_count(self) -> int:
        """
        Return the number of logical lines.
        """

        return len(self.lines)

    def get_line(self, row: int) -> str:
        """
        Safely return a line.
        """

        if 0 <= row < len(self.lines):
            return self.lines[row]

        return ""