from desktop.shell.desktop import Desktop
from desktop.ui.window.window import Window

class DummyRenderer:
    pass

class DummyEvent:
    handled = False

def main():

    desktop = Desktop()

    browser = Window("Browser")

    desktop.add_window(browser)

    assert len(desktop.window_manager.windows) == 1

    desktop.draw(DummyRenderer())

    desktop.update(0.016)

    desktop.handle_event(DummyEvent())

    desktop.remove_window(browser)

    assert len(desktop.window_manager.windows) == 0

    print("Desktop tests passed.")

if __name__ == "__main__":
    main()
