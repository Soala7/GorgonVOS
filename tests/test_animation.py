from desktop.ui.core.animation import Animation

def main():

    animation = Animation(2.0)

    animation.start()

    assert animation.playing

    animation.update(1.0)

    assert animation.progress == 0.5

    animation.update(1.0)

    assert animation.finished
    assert not animation.playing
    assert animation.progress == 1.0

    animation.reset()

    assert animation.progress == 0.0
    assert not animation.playing

    print("Animation tests passed.")

if __name__ == "__main__":
    main()
