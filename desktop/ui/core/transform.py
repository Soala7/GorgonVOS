"""
Gorgon OS (VOS)

File: transform.py
Description: Spatial transform used by every UI component.
Author: Soala Amachree & OpenAI
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field

from desktop.ui.utils.geometry import Point, Size, Rect

@dataclass(slots=True)
class Transform:
    """
    Stores the spatial state of a UI object.

    A Transform contains no rendering or event logic.
    """

    position: Point = field(default_factory=Point)
    size: Size = field(default_factory=Size)

    pivot: Point = field(
        default_factory=lambda: Point(0.5, 0.5)
    )

    scale: Point = field(
        default_factory=lambda: Point(1.0, 1.0)
    )

    rotation: float = 0.0

    _opacity: float = 1.0

    visible: bool = True
    enabled: bool = True

    dirty: bool = True

    z_index: int = 0

    def move(self, dx: float, dy: float) -> None:
        self.position.translate(dx, dy)
        self.mark_dirty()

    def move_to(self, x: float, y: float) -> None:
        self.position.x = x
        self.position.y = y
        self.mark_dirty()

    def resize(self, width: float, height: float) -> None:
        self.size.width = max(0.0, width)
        self.size.height = max(0.0, height)
        self.mark_dirty()

    def set_size(self, size: Size) -> None:
        self.size = size.copy()
        self.mark_dirty()

    def set_scale(self, sx: float, sy: float | None = None) -> None:
        if sy is None:
            sy = sx

        self.scale.x = sx
        self.scale.y = sy

        self.mark_dirty()

    def rotate(self, angle: float) -> None:
        self.rotation += angle
        self.mark_dirty()

    def set_rotation(self, angle: float) -> None:
        self.rotation = angle
        self.mark_dirty()

    def show(self) -> None:
        self.visible = True
        self.mark_dirty()

    def hide(self) -> None:
        self.visible = False
        self.mark_dirty()

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    @property
    def opacity(self) -> float:
        return self._opacity

    @opacity.setter
    def opacity(self, value: float) -> None:
        value = max(0.0, min(1.0, value))

        if value != self._opacity:
            self._opacity = value
            self.mark_dirty()

    def mark_dirty(self) -> None:
        self.dirty = True

    def clear_dirty(self) -> None:
        self.dirty = False

    def bounds(self) -> Rect:
        """
        Returns the current bounding rectangle of this transform.
        """

        return Rect(
            self.position.x,
            self.position.y,
            self.size.width,
            self.size.height,
        )
    def reset(self) -> None:
        self.position = Point()

        self.size = Size()

        self.pivot = Point(0.5, 0.5)

        self.scale = Point(1.0, 1.0)

        self.rotation = 0.0

        self.visible = True

        self.enabled = True

        self.opacity = 1.0

        self.z_index = 0

        self.mark_dirty()

    def copy(self) -> "Transform":
        clone = Transform()

        clone.position = self.position.copy()
        clone.size = self.size.copy()
        clone.pivot = self.pivot.copy()
        clone.scale = self.scale.copy()

        clone.rotation = self.rotation

        clone.opacity = self.opacity

        clone.visible = self.visible
        clone.enabled = self.enabled

        clone.z_index = self.z_index

        clone.dirty = self.dirty

        return clone
