from desktop.renderer.renderer import Renderer

class DummyRenderer(Renderer):

    def begin_frame(self):
        pass

    def end_frame(self):
        pass

    def clear(self, color):
        pass

    def draw_rect(self, rect, color):
        pass

    def draw_rect_outline(self, rect, color, width=1):
        pass

    def draw_text(
        self,
        text,
        font,
        color,
        position,
        align="left",
    ):
        pass

    def draw_image(
        self,
        image,
        bounds,
        keep_aspect=True,
    ):
        pass

    def draw_textbox(
        self,
        bounds,
        text,
        placeholder,
        focused,
    ):
        pass

def main():

    renderer = DummyRenderer()

    renderer.begin_frame()
    renderer.clear((0, 0, 0))
    renderer.end_frame()

    print("Renderer tests passed.")

if __name__ == "__main__":
    main()
