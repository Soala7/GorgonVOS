from desktop.ui.window.titlebar import TitleBar

def main():

    bar = TitleBar("Browser")

    assert bar.title == "Browser"

    bar.title = "Explorer"

    assert bar.title == "Explorer"

    assert len(bar.children) == 1

    print("TitleBar tests passed.")

if __name__ == "__main__":
    main()
