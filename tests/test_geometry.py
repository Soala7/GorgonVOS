from desktop.ui.utils.geometry import Point, Rect

def main():
    p1 = Point(0, 0)
    p2 = Point(3, 4)

    assert p1.distance_to(p2) == 5

    r1 = Rect(0, 0, 100, 100)
    r2 = Rect(50, 50, 100, 100)
    r3 = Rect(150, 150, 50, 50)

    assert r1.intersects(r2)
    assert not r1.intersects(r3)

    assert r1.contains(Point(20, 20))
    assert not r1.contains(Point(200, 200))

    r1.move(10, 15)

    assert r1.x == 10
    assert r1.y == 15

    print("Geometry tests passed.")

if __name__ == "__main__":
    main()
