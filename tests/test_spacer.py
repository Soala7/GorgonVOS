from desktop.ui.widgets.spacer import Spacer

class DummyRenderer:
    pass

def main():

    spacer = Spacer(25, 40)

    assert spacer.transform.size.width == 25
    assert spacer.transform.size.height == 40

    spacer.on_draw(DummyRenderer())

    print("Spacer tests passed.")

if __name__ == "__main__":
    main()
