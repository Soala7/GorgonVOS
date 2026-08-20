from desktop.ui.window.window import Window
from desktop.ui.window.window_buttons import WindowButtons

def main():

    window = Window()

    buttons = WindowButtons(window)

    assert len(buttons.children) == 3

    buttons.minimize_button.click()

    assert window.minimized

    buttons.maximize_button.click()

    assert window.maximized

    buttons.maximize_button.click()

    assert not window.maximized

    buttons.close_button.click()

    assert window.closed

    print("WindowButtons tests passed.")

if __name__ == "__main__":
    main()
