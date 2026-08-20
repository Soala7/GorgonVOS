from desktop.ui.window.window import Window

def main():

    window = Window(
        title="Browser",
        width=1200,
        height=700,
    )

    assert window.title == "Browser"

    assert window.transform.size.width == 1200
    assert window.transform.size.height == 700

    window.minimize()

    assert window.minimized

    window.restore()

    assert not window.minimized

    window.maximize()

    assert window.maximized

    window.activate()

    assert window.active

    window.deactivate()

    assert not window.active

    window.close()

    assert window.closed
    assert window.destroyed

    print("Window tests passed.")

if __name__ == "__main__":
    main()
