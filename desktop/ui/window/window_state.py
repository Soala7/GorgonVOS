"""
Gorgon OS (VOS)

Window State
"""

from __future__ import annotations

from enum import Enum, auto

class WindowState(Enum):
    """
    Possible window states.
    """

    NORMAL = auto()

    MINIMIZED = auto()

    MAXIMIZED = auto()

    FULLSCREEN = auto()

    CLOSED = auto()
