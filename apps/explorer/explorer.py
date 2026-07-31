"""
VOS Explorer Application
"""

from apps.explorer.explorer_window import ExplorerWindow


class Explorer:

    def __init__(self):

        self.window = ExplorerWindow()

        self.window_manager = None


    def open(self):

        print("Opening explorer")

        if not self.window_manager:

            print("No WindowManager")
            return


        if self.window in self.window_manager.windows:

            print("Already open")

            if self.window_manager.active_window is self.window:

                self.close()
                return


            self.window_manager.focus_window(
                self.window
            )

            return


        print("Adding window")


        if self.window.closed:

            self.window = ExplorerWindow()


        self.window.restore()


        self.window_manager.add_window(
            self.window
        )


        self.window_manager.focus_window(
            self.window
        )


    def close(self):

        if self.window_manager:

            self.window_manager.close_window(
                self.window
            )


    def update(self, dt):

        self.window.update(dt)


    def draw(self, renderer):

        self.window.draw(renderer)


    def handle_event(self, event):

        self.window.handle_event(event)