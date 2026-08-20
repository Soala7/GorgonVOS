"""
Gorgon OS (VOS)

Renderer Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod

class Renderer(ABC):
    """
    Base renderer interface.
    """

    @abstractmethod
    def begin_frame(self) -> None:
        pass

    @abstractmethod
    def end_frame(self) -> None:
        pass

    @abstractmethod
    def clear(self, color) -> None:
        pass

    @abstractmethod
    def draw_rect(self, rect, color) -> None:
        pass

    @abstractmethod
    def draw_rect_outline(self, rect, color, width=1) -> None:
        pass

    @abstractmethod
    def draw_text(
        self,
        text,
        font,
        color,
        position,
        align="left",
    ) -> None:
        pass

    @abstractmethod
    def draw_image(
        self,
        image,
        bounds,
        keep_aspect=True,
    ) -> None:
        pass

    @abstractmethod
    def draw_textbox(
        self,
        bounds,
        text,
        placeholder,
        focused,
    ) -> None:
        pass
