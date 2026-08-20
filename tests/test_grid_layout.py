from desktop.ui.layout.grid_layout import GridLayout
from desktop.ui.core.container import Container
from desktop.ui.core.component import Component

def main():

    container = Container()

    layout = GridLayout(
        columns=2,
        spacing=10,
        margin=5,
    )

    children = []

    for i in range(4):

        c = Component(str(i))

        c.transform.resize(50, 20)

        container.add_child(c)

        children.append(c)

    layout.apply(container)

    assert children[0].transform.position.x == 5
    assert children[0].transform.position.y == 5

    assert children[1].transform.position.x == 65
    assert children[1].transform.position.y == 5

    assert children[2].transform.position.x == 5
    assert children[2].transform.position.y == 35

    assert children[3].transform.position.x == 65
    assert children[3].transform.position.y == 35

    print("Grid layout tests passed.")

if __name__ == "__main__":
    main()
