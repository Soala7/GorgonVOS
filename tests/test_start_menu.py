from desktop.shell.start_menu import StartMenu
from desktop.ui.widgets.button import Button

def main():

    menu = StartMenu()

    assert not menu.visible

    menu.open()

    assert menu.visible

    menu.close()

    assert not menu.visible

    menu.toggle()

    assert menu.visible

    browser = Button("Browser")

    menu.add_item(browser)

    assert len(menu.children) == 1

    print("StartMenu tests passed.")

if __name__ == "__main__":
    main()
