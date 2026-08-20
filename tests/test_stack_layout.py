from desktop.ui.layout.stack_layout import StackLayout
from desktop.ui.core.container import Container
from desktop.ui.core.component import Component

def main():

    container = Container()

    layout = StackLayout(margin=10)

    children = []

    for i in range(5):

        component = Component(str(i))

        container.add_child(component)

        children.append(component)

    layout.apply(container)

    for child in children:

        assert child.transform.position.x == 10
        assert child.transform.position.y == 10

    print("Stack layout tests passed.")

if __name__ == "__main__":
    main()
