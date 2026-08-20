from desktop.ui.core.component import Component
from desktop.ui.core.focus import FocusManager

def main():

    manager = FocusManager()

    a = Component("A")
    b = Component("B")

    manager.set_focus(a)

    assert manager.focused is a
    assert a.focused

    manager.set_focus(b)

    assert not a.focused
    assert b.focused

    manager.clear_focus()

    assert manager.focused is None

    print("Focus tests passed.")

if __name__ == "__main__":
    main()
