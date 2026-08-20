"""
Gorgon OS (VOS)

Textbox widget.
"""

from __future__ import annotations

from desktop.ui.core.event import KeyPressEvent
from desktop.ui.widgets.widget import Widget

class TextBox(Widget):
    """
    Simple text input widget.
    """

    def __init__(
        self,
        text: str = "",
        placeholder: str = "",
        name: str = "TextBox",
    ) -> None:

        super().__init__(name)

        self.focusable = True

        self.text = text

        self.placeholder = placeholder

        self.cursor_position = len(text)

    def insert(self, text: str) -> None:

        self.text = (
            self.text[:self.cursor_position]
            + text
            + self.text[self.cursor_position:]
        )

        self.cursor_position += len(text)

    def backspace(self) -> None:

        if self.cursor_position == 0:
            return

        self.text = (
            self.text[: self.cursor_position - 1]
            + self.text[self.cursor_position :]
        )

        self.cursor_position -= 1

    def clear(self) -> None:

        self.text = ""

        self.cursor_position = 0

    def handle_event(self, event) -> None:

        super().handle_event(event)

        if not isinstance(event, KeyPressEvent):
            return

        if event.key == "BACKSPACE":

            self.backspace()

        elif len(event.key) == 1:

            self.insert(event.key)

    def on_draw(self, renderer) -> None:

        renderer.draw_textbox(
            bounds=self.transform.bounds,
            text=self.text,
            placeholder=self.placeholder,
            focused=self.focused,
        )
