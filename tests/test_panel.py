from desktop.ui.widgets.panel import Panel

class DummyRenderer:

    def draw_rect(self, *args):
        pass

    def draw_rect_outline(self, *args):
        pass

def main():

    panel = Panel()

    panel.set_background((30, 30, 30))

    panel.set_border((255, 255, 255), 2)

    renderer = DummyRenderer()

    panel.draw(renderer)

    panel.clear_border()

    assert panel.border_width == 0

    print("Panel tests passed.")

if __name__ == "__main__":
    main()
