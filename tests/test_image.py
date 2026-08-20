from desktop.ui.widgets.image import Image

class DummyRenderer:

    def draw_image(
        self,
        image,
        bounds,
        keep_aspect,
    ):
        pass

def main():

    image = Image()

    image.set_image(object())

    renderer = DummyRenderer()

    image.draw(renderer)

    assert image.image is not None

    image.clear_image()

    assert image.image is None

    print("Image tests passed.")

if __name__ == "__main__":
    main()
