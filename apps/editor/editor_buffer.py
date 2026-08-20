
from __future__ import annotations

class EditorBuffer:
    """Manages raw text lines, cursor position, and mutation history."""

    def __init__(self, content: str = "") -> None:
        self.lines: list[str] = []
        self.set_text(content)
        self.cursor_row: int = 0
        self.cursor_col: int = 0
        self.is_dirty: bool = False

    def set_text(self, content: str) -> None:
        """Replace buffer contents with raw text."""
        cleaned = content.replace("\r\n", "\n").replace("\r", "\n")
        self.lines = cleaned.split("\n") if cleaned else [""]
        self.cursor_row = 0
        self.cursor_col = 0
        self.is_dirty = False

    def get_text(self) -> str:
        """Get full buffer text as a single string."""
        return "\n".join(self.lines)

    def insert_char(self, ch: str) -> None:
        """Insert printable characters at the active cursor position."""
        line = self.lines[self.cursor_row]
        self.lines[self.cursor_row] = (
            line[: self.cursor_col] + ch + line[self.cursor_col :]
        )
        self.cursor_col += len(ch)
        self.is_dirty = True

    def insert_newline(self) -> None:
        """Split the current line at the cursor."""
        line = self.lines[self.cursor_row]
        left, right = line[: self.cursor_col], line[self.cursor_col :]
        self.lines[self.cursor_row] = left
        self.lines.insert(self.cursor_row + 1, right)
        self.cursor_row += 1
        self.cursor_col = 0
        self.is_dirty = True

    def delete_backspace(self) -> None:
        """Delete character behind the cursor or merge with previous line."""
        if self.cursor_col > 0:
            line = self.lines[self.cursor_row]
            self.lines[self.cursor_row] = (
                line[: self.cursor_col - 1] + line[self.cursor_col :]
            )
            self.cursor_col -= 1
            self.is_dirty = True
        elif self.cursor_row > 0:
            prev_line = self.lines[self.cursor_row - 1]
            curr_line = self.lines.pop(self.cursor_row)
            self.cursor_row -= 1
            self.cursor_col = len(prev_line)
            self.lines[self.cursor_row] = prev_line + curr_line
            self.is_dirty = True

    def delete_forward(self) -> None:
        """Delete character ahead of the cursor or pull up next line."""
        line = self.lines[self.cursor_row]
        if self.cursor_col < len(line):
            self.lines[self.cursor_row] = (
                line[: self.cursor_col] + line[self.cursor_col + 1 :]
            )
            self.is_dirty = True
        elif self.cursor_row < len(self.lines) - 1:
            self.lines[self.cursor_row] += self.lines.pop(self.cursor_row + 1)
            self.is_dirty = True
