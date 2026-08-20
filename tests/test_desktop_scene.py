from boot.desktop_scene import DesktopScene

class DummyRenderer:
    pass

class DummyEvent:

    handled = False

def main():

    scene = DesktopScene()

    scene.update(0.016)

    scene.draw(DummyRenderer())

    scene.handle_event(DummyEvent())

    print("DesktopScene tests passed.")

if __name__ == "__main__":
    main()
