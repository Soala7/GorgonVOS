"""
Gorgon OS (VOS)

Base widget class.
"""

from __future__ import annotations

from desktop.ui.core.component import Component

class Widget(Component):
    """
    Base class for all interactive UI widgets.
    """

    def __init__(self, name: str = "Widget") -> None:
        super().__init__(name)

        self.enabled = True

    def enable(self) -> None:
        self.enabled = True
        self.on_enable()

    def disable(self) -> None:
        self.enabled = False
        self.on_disable()

    def toggle(self) -> None:
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def is_enabled(self) -> bool:
        return self.enabled
