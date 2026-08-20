from desktop.ui.window.resize_handle import ResizeHandle

def main():

    handle = ResizeHandle()

    assert handle.edge == "bottom_right"

    assert not handle.dragging

    handle.start_resize()

    assert handle.dragging

    handle.stop_resize()

    assert not handle.dragging

    print("ResizeHandle tests passed.")

if __name__ == "__main__":
    main()
