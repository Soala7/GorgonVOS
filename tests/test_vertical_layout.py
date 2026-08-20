from desktop.ui.layout.vertical_layout import VerticalLayout
from desktop.ui.core.container import Container
from desktop.ui.core.component import Component

def main():

    container = Container()

    layout = VerticalLayout(
        spacing=10,
        margin=5,
    )

    a = Component("A")
    b = Component("B")
    c = Component("C")

    a.transform.resize(100, 20)
    b.transform.resize(100, 30)
    c.transform.resize(100, 40)

    container.add_child(a)
    container.add_child(b)
    container.add_child(c)

    layout.apply(container)

    assert a.transform.position.y == 5
    assert b.transform.position.y == 35
    assert c.transform.position.y == 75

    print("Vertical layout tests passed.")

if __name__ == "__main__":
    main()
