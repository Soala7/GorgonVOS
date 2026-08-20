from desktop.ui.widgets.widget import Widget

def main():

    widget = Widget()

    assert widget.is_enabled()

    widget.disable()

    assert not widget.is_enabled()

    widget.enable()

    assert widget.is_enabled()

    widget.toggle()

    assert not widget.is_enabled()

    widget.toggle()

    assert widget.is_enabled()

    print("Widget tests passed.")

if __name__ == "__main__":
    main()
