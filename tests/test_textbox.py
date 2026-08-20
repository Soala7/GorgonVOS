from desktop.ui.widgets.textbox import TextBox
from desktop.ui.core.event import KeyPressEvent

class DummyRenderer:

    def draw_textbox(self, **kwargs):
        pass

def main():

    textbox = TextBox()

    textbox.insert("H")
    textbox.insert("i")

    assert textbox.text == "Hi"

    textbox.backspace()

    assert textbox.text == "H"

    textbox.handle_event(KeyPressEvent("i"))

    assert textbox.text == "Hi"

    textbox.clear()

    assert textbox.text == ""

    textbox.on_draw(DummyRenderer())

    print("Textbox tests passed.")

if __name__ == "__main__":
    main()
