from desktop.shell.shell import Shell

class DummyRenderer:
    pass

class DummyEvent:
    handled = False

def main():

    shell = Shell()

    assert shell.desktop is not None
    assert shell.taskbar is not None
    assert shell.start_menu is not None
    assert shell.notification_center is not None
    assert shell.desktop_icons is not None

    shell.update(0.016)

    shell.draw(DummyRenderer())

    shell.handle_event(DummyEvent())

    print("Shell tests passed.")

if __name__ == "__main__":
    main()
