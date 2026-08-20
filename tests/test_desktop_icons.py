from desktop.shell.desktop_icons import DesktopIcons
from desktop.ui.widgets.button import Button

def main():

    icons = DesktopIcons()

    browser = Button("Browser")
    terminal = Button("Terminal")

    icons.add_icon(browser)
    icons.add_icon(terminal)

    assert len(icons.children) == 2

    icons.remove_icon(browser)

    assert len(icons.children) == 1

    icons.clear_icons()

    assert len(icons.children) == 0

    print("DesktopIcons tests passed.")

if __name__ == "__main__":
    main()
