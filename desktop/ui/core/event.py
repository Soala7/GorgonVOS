"""
Gorgon OS (VOS)

File: event.py
Description: Defines all UI event types used by the Gorgon OS UI framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from time import monotonic
from typing import Any

class EventType(Enum):
    MOUSE_MOVE = auto()
    MOUSE_PRESS = auto()
    MOUSE_RELEASE = auto()
    MOUSE_DOUBLE_CLICK = auto()
    MOUSE_WHEEL = auto()

    KEY_PRESS = auto()
    KEY_RELEASE = auto()
    MOUSE_CLICK = auto()

    WINDOW_MOVE = auto()
    WINDOW_RESIZE = auto()
    WINDOW_CLOSE = auto()
    WINDOW_FOCUS = auto()
    WINDOW_BLUR = auto()

    CUSTOM = auto()

class MouseButton(Enum):
    NONE = auto()
    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()
    X1 = auto()
    X2 = auto()

class KeyModifier(Enum):
    NONE = auto()
    SHIFT = auto()
    CTRL = auto()
    ALT = auto()
    SUPER = auto()

@dataclass(slots=True)
class UIEvent:
    event_type: EventType
    handled: bool = False
    timestamp: float = field(default_factory=monotonic)
    source: Any | None = None

    def stop_propagation(self) -> None:
        self.handled = True

@dataclass(slots=True)
class MouseEvent(UIEvent):
    x: float = 0.0
    y: float = 0.0
    button: MouseButton = MouseButton.NONE

class MouseMoveEvent(MouseEvent):
    def __init__(self, x: float, y: float):
        self._init_base(
            EventType.MOUSE_MOVE,
            x=x,
            y=y,
        )

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.x = kwargs.get("x", 0.0)
        self.y = kwargs.get("y", 0.0)
        self.button = MouseButton.NONE

class MousePressEvent(MouseEvent):
    def __init__(self, x: float, y: float, button: MouseButton):
        self._init_base(
            EventType.MOUSE_PRESS,
            x=x,
            y=y,
            button=button,
        )

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.x = kwargs.get("x", 0.0)
        self.y = kwargs.get("y", 0.0)
        self.button = kwargs.get("button", MouseButton.NONE)

class MouseReleaseEvent(MouseEvent):
    def __init__(self, x: float, y: float, button: MouseButton):
        self._init_base(
            EventType.MOUSE_RELEASE,
            x=x,
            y=y,
            button=button,
        )

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.x = kwargs.get("x", 0.0)
        self.y = kwargs.get("y", 0.0)
        self.button = kwargs.get("button", MouseButton.NONE)

class MouseWheelEvent(MouseEvent):
    def __init__(self, x: float, y: float, delta: int):
        self._init_base(
            EventType.MOUSE_WHEEL,
            x=x,
            y=y,
            button=MouseButton.NONE,
        )
        self.delta = delta

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.x = kwargs.get("x", 0.0)
        self.y = kwargs.get("y", 0.0)
        self.button = MouseButton.NONE

class MouseDoubleClickEvent(MouseEvent):
    def __init__(self, x: float, y: float, button: MouseButton):
        self._init_base(
            EventType.MOUSE_DOUBLE_CLICK,
            x=x,
            y=y,
            button=button,
        )

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.x = kwargs.get("x", 0.0)
        self.y = kwargs.get("y", 0.0)
        self.button = kwargs.get("button", MouseButton.NONE)

@dataclass(slots=True)
class KeyboardEvent(UIEvent):
    key: int = 0
    unicode: str = ""
    modifier: KeyModifier = KeyModifier.NONE

class KeyPressEvent(KeyboardEvent):

    def __init__(
        self,
        key: int,
        unicode: str = "",
        modifier: KeyModifier = KeyModifier.NONE,
    ):

        self._init_base(
            EventType.KEY_PRESS,
            key=key,
            unicode=unicode,
            modifier=modifier,
        )

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.key = kwargs.get("key", 0)
        self.unicode = kwargs.get("unicode")or("")
        self.modifier = kwargs.get("modifier", KeyModifier.NONE)

class KeyReleaseEvent(KeyboardEvent):
    def __init__(self, key: int, modifier: KeyModifier = KeyModifier.NONE):
        self._init_base(
            EventType.KEY_RELEASE,
            key=key,
            modifier=modifier,
        )

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.key = kwargs.get("key", 0)
        self.modifier = kwargs.get("modifier", KeyModifier.NONE)

@dataclass(slots=True)
class MouseEvent(UIEvent):
    x: float = 0
    y: float = 0

class MouseClickEvent(UIEvent):

    def __init__(self, x: float, y: float):
        self.event_type = EventType.MOUSE_CLICK
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.x = x
        self.y = y

@dataclass(slots=True)
class WindowEvent(UIEvent):
    window_id: int = -1

class WindowMoveEvent(WindowEvent):
    def __init__(self, window_id: int, x: float, y: float):
        self._init_base(
            EventType.WINDOW_MOVE,
            window_id=window_id,
            x=x,
            y=y,
        )

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.window_id = kwargs.get("window_id", -1)
        self.x = kwargs.get("x", 0.0)
        self.y = kwargs.get("y", 0.0)

class WindowResizeEvent(WindowEvent):
    def __init__(self, window_id: int, width: float, height: float):
        self._init_base(
            EventType.WINDOW_RESIZE,
            window_id=window_id,
            width=width,
            height=height,
        )

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.window_id = kwargs.get("window_id", -1)
        self.width = kwargs.get("width", 0.0)
        self.height = kwargs.get("height", 0.0)

class WindowFocusEvent(WindowEvent):
    def __init__(self, window_id: int):
        self._init_base(EventType.WINDOW_FOCUS, window_id=window_id)

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.window_id = kwargs.get("window_id", -1)

class WindowBlurEvent(WindowEvent):
    def __init__(self, window_id: int):
        self._init_base(EventType.WINDOW_BLUR, window_id=window_id)

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.window_id = kwargs.get("window_id", -1)

class WindowCloseEvent(WindowEvent):
    def __init__(self, window_id: int):
        self._init_base(EventType.WINDOW_CLOSE, window_id=window_id)

    def _init_base(self, event_type, **kwargs):
        self.event_type = event_type
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.window_id = kwargs.get("window_id", -1)

@dataclass(slots=True)
class CustomEvent(UIEvent):
    name: str = ""
    payload: dict[str, Any] = field(default_factory=dict)

    def __init__(self, name: str, payload: dict[str, Any] | None = None):
        self.event_type = EventType.CUSTOM
        self.handled = False
        self.timestamp = monotonic()
        self.source = None
        self.name = name
        self.payload = payload or {}
