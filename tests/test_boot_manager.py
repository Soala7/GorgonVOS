import time

from boot.boot_manager import BootManager

class DummyRenderer:
    pass

class DummyEvent:
    handled = False

def main():

    manager = BootManager()

    assert manager.state == manager.BOOT

    time.sleep(3.1)

    manager.update(0.016)

    assert manager.state == manager.LOGIN

    manager.login_screen.select_user("Soala")

    manager.login_screen.login()

    manager.update(0.016)

    assert manager.state == manager.DESKTOP

    manager.draw(DummyRenderer())

    manager.handle_event(DummyEvent())

    print("BootManager tests passed.")

if __name__ == "__main__":
    main()
