from desktop.shell.taskbar import Taskbar
from desktop.ui.widgets.button import Button

def main():

    taskbar = Taskbar()

    browser = Button("Browser")

    explorer = Button("Explorer")

    taskbar.add_app(browser)

    taskbar.add_app(explorer)

    assert len(taskbar.running_apps) == 2

    assert len(taskbar.children) == 2

    taskbar.remove_app(browser)

    assert len(taskbar.running_apps) == 1

    assert len(taskbar.children) == 1

    print("Taskbar tests passed.")

if __name__ == "__main__":
    main()
