from desktop.ui.core.container import Container
from desktop.ui.core.component import Component

def main():

    root = Container()

    a = Component("A")
    b = Component("B")

    root.add_child(a)
    root.add_child(b)

    assert len(root.children) == 2

    a.destroy()

    root.update(0)

    assert len(root.children) == 1

    print("Container tests passed.")

if __name__ == "__main__":
    main()
