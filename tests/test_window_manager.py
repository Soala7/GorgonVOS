from desktop.ui.window.window import Window
from desktop.ui.window.window_manager import WindowManager

class DummyRenderer:
    pass

class DummyEvent:

    handled = False

def main():

    manager = WindowManager()

    browser = Window("Browser")

    explorer = Window("Explorer")

    manager.add_window(browser)

    manager.add_window(explorer)

    assert len(manager.windows) == 2

    assert manager.active_window is explorer

    manager.focus_window(browser)

    assert manager.active_window is browser

    assert manager.windows[-1] is browser

    manager.draw(DummyRenderer())

    manager.update(0.016)

    manager.handle_event(DummyEvent())

    manager.close_window(browser)

    assert len(manager.windows) == 1

    print("WindowManager tests passed.")

if __name__ == "__main__":
    main()
