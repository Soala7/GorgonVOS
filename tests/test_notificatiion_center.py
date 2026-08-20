from desktop.shell.notification_center import NotificationCenter
from desktop.ui.widgets.label import Label

def main():

    center = NotificationCenter()

    assert not center.visible

    center.show()

    assert center.visible

    center.hide()

    assert not center.visible

    notification = Label("Hello")

    center.add_notification(notification)

    assert len(center.children) == 1

    center.clear()

    assert len(center.children) == 0

    print("NotificationCenter tests passed.")

if __name__ == "__main__":
    main()
