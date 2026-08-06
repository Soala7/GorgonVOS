"""
VOS Text Editor Application
"""

from apps.editor.editor_window import EditorWindow


class TextEditor:

    def __init__(self, service_manager):

        self.service_manager = service_manager

        self.window = EditorWindow()

        self.window_manager = None

    def open(self):

        print("Opening editor")

        if not self.window_manager:
            print("No WindowManager")
            return

        if self.window in self.window_manager.windows:

            print("Already open")

            if self.window_manager.active_window is self.window:
                return

            self.window_manager.focus_window(self.window)
            return

        print("Adding window")

        if self.window.closed:
            self.window = EditorWindow()

        self.window.restore()

        self.window_manager.add_window(self.window)
        self.window_manager.focus_window(self.window)