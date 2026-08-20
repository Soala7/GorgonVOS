from desktop.ui.core.event import (
    MouseMoveEvent,
    MousePressEvent,
    MouseButton,
    KeyPressEvent,
    KeyModifier,
    WindowResizeEvent,
    CustomEvent,
    EventType,
)

def main():
    move = MouseMoveEvent(10, 20)
    assert move.event_type == EventType.MOUSE_MOVE
    assert move.x == 10
    assert move.y == 20

    click = MousePressEvent(100, 200, MouseButton.LEFT)
    assert click.button == MouseButton.LEFT

    key = KeyPressEvent(65, KeyModifier.CTRL)
    assert key.key == 65
    assert key.modifier == KeyModifier.CTRL

    resize = WindowResizeEvent(1, 1280, 720)
    assert resize.window_id == 1
    assert resize.width == 1280

    custom = CustomEvent(
        "browser_loaded",
        {"url": "https://example.com"},
    )

    assert custom.name == "browser_loaded"
    assert custom.payload["url"] == "https://example.com"

    custom.stop_propagation()
    assert custom.handled

    print("Event tests passed.")

if __name__ == "__main__":
    main()
