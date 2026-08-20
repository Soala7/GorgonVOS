from desktop.ui.layout.horizontal_layout import HorizontalLayout
from desktop.ui.core.container import Container
from desktop.ui.core.component import Component

def main():

    container = Container()

    layout = HorizontalLayout(
        spacing=10,
        margin=5,
    )

    a = Component("A")
    b = Component("B")
    c = Component("C")

    a.transform.resize(20, 100)
    b.transform.resize(30, 100)
    c.transform.resize(40, 100)

    container.add_child(a)
    container.add_child(b)
    container.add_child(c)

    layout.apply(container)

    assert a.transform.position.x == 5
    assert b.transform.position.x == 35
    assert c.transform.position.x == 75

    print("Horizontal layout tests passed.")

if __name__ == "__main__":
    main()
