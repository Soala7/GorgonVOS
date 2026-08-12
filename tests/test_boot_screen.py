import time

from boot.boot_screen import BootScreen


def main():

    boot = BootScreen(duration=0.5)

    boot.start()

    assert not boot.finished

    time.sleep(0.6)

    boot.update()

    assert boot.finished

    assert boot.progress == 1.0

    boot.reset()

    assert not boot.finished

    print("BootScreen tests passed.")


if __name__ == "__main__":
    main()