from desktop.ui.widgets.label import Label

class DummyRenderer:

    def draw_text(
        self,
        text,
        font,
        color,
        position,
        align,
    ):
        pass

def main():

    label = Label("Hello Gorgon OS")

    label.set_font(object())

    label.set_color((255, 255, 255))

    renderer = DummyRenderer()

    label.draw(renderer)

    assert label.text == "Hello Gorgon OS"

    print("Label tests passed.")

if __name__ == "__main__":
    main()
