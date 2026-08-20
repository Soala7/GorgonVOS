"""
Gorgon OS (VOS)

Container component.
"""

from __future__ import annotations

from desktop.ui.core.component import Component
from desktop.ui.core.event import UIEvent

class Container(Component):
    """
    A component that owns and manages child components.
    """

    def __init__(self, name: str = "Container") -> None:
        super().__init__(name)

    def update(self, dt: float) -> None:
        self.on_update(dt)

        destroyed = []

        for child in self.children:
            child.update(dt)

            if child.destroyed:
                destroyed.append(child)

        for child in destroyed:
            self.remove_child(child)

    def draw(self, renderer) -> None:
        self.on_draw(renderer)

        for child in self.children:
            child.draw(renderer)

    def handle_event(self, event: UIEvent) -> None:

        for child in reversed(self.children):

            if event.handled:
                break

            child.handle_event(event)
