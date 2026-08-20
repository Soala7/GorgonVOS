"""
Gorgon OS (VOS)

File: geometry.py
Description: Fundamental geometry classes used throughout the UI framework.
Author: Soala Amachree & OpenAI
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

@dataclass(slots=True)
class Point:
    x: float = 0.0
    y: float = 0.0

    def copy(self) -> "Point":
        return Point(self.x, self.y)

    def translate(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy

    def distance_to(self, other: "Point") -> float:
        return hypot(other.x - self.x, other.y - self.y)

    def tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

@dataclass(slots=True)
class Size:
    width: float = 0.0
    height: float = 0.0

    def copy(self) -> "Size":
        return Size(self.width, self.height)

    def tuple(self) -> tuple[float, float]:
        return (self.width, self.height)

    @property
    def is_empty(self) -> bool:
        return self.width <= 0 or self.height <= 0

@dataclass(slots=True)
class Rect:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    @property
    def left(self) -> float:
        return self.x

    @property
    def top(self) -> float:
        return self.y

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center(self) -> Point:
        return Point(
            self.x + self.width / 2,
            self.y + self.height / 2,
        )

    @property
    def size(self) -> Size:
        return Size(self.width, self.height)

    @property
    def position(self) -> Point:
        return Point(self.x, self.y)

    def copy(self) -> "Rect":
        return Rect(
            self.x,
            self.y,
            self.width,
            self.height,
        )

    def tuple(self) -> tuple[float, float, float, float]:
        return (
            self.x,
            self.y,
            self.width,
            self.height,
        )

    def move(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy

    def move_to(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def resize(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def inflate(self, dw: float, dh: float) -> None:
        self.x -= dw / 2
        self.y -= dh / 2
        self.width += dw
        self.height += dh

    def contains(self, point: Point) -> bool:
        return (
            self.left <= point.x <= self.right
            and self.top <= point.y <= self.bottom
        )

    def intersects(self, other: "Rect") -> bool:
        return not (
            self.right <= other.left
            or self.left >= other.right
            or self.bottom <= other.top
            or self.top >= other.bottom
        )

@dataclass(slots=True)
class Padding:
    left: float = 0.0
    top: float = 0.0
    right: float = 0.0
    bottom: float = 0.0

    @property
    def horizontal(self) -> float:
        return self.left + self.right

    @property
    def vertical(self) -> float:
        return self.top + self.bottom

@dataclass(slots=True)
class Margin:
    left: float = 0.0
    top: float = 0.0
    right: float = 0.0
    bottom: float = 0.0

    @property
    def horizontal(self) -> float:
        return self.left + self.right

    @property
    def vertical(self) -> float:
        return self.top + self.bottom
