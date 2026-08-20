"""
Gorgon OS (VOS)

File: component.py
Description: Base class for every visible UI object.
Author: Soala Amachree & OpenAI
License: MIT
"""

from __future__ import annotations

from typing import Any

from desktop.ui.core.event import UIEvent
from desktop.ui.core.transform import Transform
from desktop.ui.utils.geometry import Point

class Component:
    """Base class for every UI component."""

    _next_id: int = 1

    def __init__(self, name: str = "Component") -> None:

        self.id: int = Component._next_id
        Component._next_id += 1

        self.name: str = name

        self.parent: Component | None = None
        self.children: list[Component] = []

        self.layer: int = 0

        self.transform = Transform()

        self.focusable = False

        self.hovered = False
        self.focused = False
        self.pressed = False

        self._destroyed = False

        self.tooltip = ""

        self.cursor = None

        self.user_data: dict[str, Any] = {}

        self.on_create()

    def add_child(self, child: "Component") -> None:

        if child.parent is not None:
            child.parent.remove_child(child)

        child.parent = self

        self.children.append(child)

    def remove_child(self, child: "Component") -> None:

        if child in self.children:

            self.children.remove(child)

            child.parent = None

    def clear_children(self) -> None:

        for child in self.children:
            child.parent = None

        self.children.clear()

    def find_by_id(self, component_id: int) -> "Component | None":

        if self.id == component_id:
            return self

        for child in self.children:

            result = child.find_by_id(component_id)

            if result is not None:
                return result

        return None

    def find_by_name(self, name: str) -> "Component | None":

        if self.name == name:
            return self

        for child in self.children:

            result = child.find_by_name(name)

            if result is not None:
                return result

        return None

    def contains_point(self, point: Point) -> bool:
        return self.transform.bounds.contains(point)

    def global_position(self) -> Point:

        x = self.transform.position.x
        y = self.transform.position.y

        parent = self.parent

        while parent is not None:

            x += parent.transform.position.x
            y += parent.transform.position.y

            parent = parent.parent

        return Point(x, y)

    def update(self, dt: float) -> None:

        self.on_update(dt)

        for child in self.children:
            child.update(dt)

    def draw(self, renderer) -> None:

        self.on_draw(renderer)

        for child in sorted(
            self.children,
            key=lambda c: c.layer,
        ):
            child.draw(renderer)

    def handle_event(self, event: UIEvent) -> None:

        for child in reversed(self.children):

            if event.handled:
                return

            child.handle_event(event)

    def destroy(self) -> None:

        self._destroyed = True

        self.on_destroy()

    @property
    def destroyed(self) -> bool:
        return self._destroyed

    def on_create(self) -> None:
        pass

    def on_update(self, dt: float) -> None:
        pass

    def on_draw(self, renderer) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def on_focus(self) -> None:
        pass

    def on_blur(self) -> None:
        pass

    def on_enable(self) -> None:
        pass

    def on_disable(self) -> None:
        pass

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"name='{self.name}')"
        )
