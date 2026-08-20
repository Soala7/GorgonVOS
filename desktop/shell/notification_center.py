"""
Gorgon OS (VOS)

Notification Center
"""

from __future__ import annotations

from desktop.ui.widgets.panel import Panel
from desktop.ui.layout.vertical_layout import VerticalLayout

class NotificationCenter(Panel):
    """
    Displays desktop notifications.
    """

    def __init__(self) -> None:

        super().__init__("NotificationCenter")

        self.visible = False

        self.layout = VerticalLayout(
            spacing=4,
            margin=8,
        )

    def show(self) -> None:

        self.visible = True

    def hide(self) -> None:

        self.visible = False

    def toggle(self) -> None:

        self.visible = not self.visible

    def add_notification(self, notification) -> None:

        self.add_child(notification)

        self.layout.apply(self)

    def clear(self) -> None:

        self.clear_children()
