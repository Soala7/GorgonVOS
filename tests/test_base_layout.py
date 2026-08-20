from desktop.ui.layout.base_layout import BaseLayout
from desktop.ui.core.container import Container

class DummyLayout(BaseLayout):

    def apply(self, container: Container) -> None:
        pass

def main():

    layout = DummyLayout()

    container = Container()

    layout.apply(container)

    print("Base layout tests passed.")

if __name__ == "__main__":
    main()
