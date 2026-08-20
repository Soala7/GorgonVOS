from desktop.shell.wallpaper import Wallpaper

def main():

    wallpaper = Wallpaper()

    assert wallpaper.keep_aspect is False

    wallpaper.set_image(object())

    assert wallpaper.image is not None

    print("Wallpaper tests passed.")

if __name__ == "__main__":
    main()
