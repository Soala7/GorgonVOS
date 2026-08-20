from desktop.ui.window.window_state import WindowState

def main():

    assert WindowState.NORMAL != WindowState.MINIMIZED
    assert WindowState.MAXIMIZED != WindowState.CLOSED
    assert WindowState.FULLSCREEN.name == "FULLSCREEN"

    print("WindowState tests passed.")

if __name__ == "__main__":
    main()
