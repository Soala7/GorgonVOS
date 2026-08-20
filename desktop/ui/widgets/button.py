"""
Gorgon OS (VOS)

Button widget.
"""

from __future__ import annotations

from desktop.ui.widgets.label import Label
from desktop.ui.core.event import MousePressEvent, MouseReleaseEvent

class Button(Label):
    """
    Basic clickable button.
    """

    def __init__(
        self,
        text: str = "Button",
        name: str = "Button",
    ) -> None:

        super().__init__(text, name)

        self.focusable = True

        self.pressed = False

        self.on_click = None

    def click(self) -> None:

        if callable(self.on_click):
            self.on_click()

    def handle_event(self, event) -> None:

        super().handle_event(event)

        if isinstance(event, MousePressEvent):

            self.pressed = True

            event.handled = True

        elif isinstance(event, MouseReleaseEvent):

            if self.pressed:

                self.pressed = False

                self.click()

                event.handled = True
