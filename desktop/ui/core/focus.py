"""
Gorgon OS (VOS)

Focus Manager
"""

from __future__ import annotations

from desktop.ui.core.component import Component

class FocusManager:
    """
    Manages keyboard focus.
    """

    def __init__(self) -> None:
        self._focused: Component | None = None

    @property
    def focused(self) -> Component | None:
        return self._focused

    def has_focus(self) -> bool:
        return self._focused is not None

    def set_focus(self, component: Component | None) -> None:

        if component is self._focused:
            return

        if self._focused is not None:
            self._focused.focused = False
            self._focused.on_blur()

        self._focused = component

        if component is not None:
            component.focused = True
            component.on_focus()

    def clear_focus(self) -> None:
        self.set_focus(None)

    def is_focused(self, component: Component) -> bool:
        return self._focused is component
