from desktop.ui.widgets.button import Button
from desktop.ui.core.event import (
    MousePressEvent,
    MouseReleaseEvent,
)

def main():

    clicked = False

    def callback():
        nonlocal clicked
        clicked = True

    button = Button("OK")

    button.on_click = callback

    press = MousePressEvent(
        button=1,
        x=0,
        y=0,
    )

    release = MouseReleaseEvent(
        button=1,
        x=0,
        y=0,
    )

    button.handle_event(press)

    assert button.pressed

    button.handle_event(release)

    assert not button.pressed

    assert clicked

    print("Button tests passed.")

if __name__ == "__main__":
    main()
