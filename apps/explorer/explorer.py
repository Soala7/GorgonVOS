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

    # apps/explorer/explorer_window.py (or apps/explorer.py)

    def _on_item_double_click(self, selected_item):
        """Handles double clicking an item in the file view."""
        
        # 1. Skip folders (navigate into them instead)
        if getattr(selected_item, "is_directory", False) or hasattr(selected_item, "children"):
            self.navigate_to(selected_item)
            return

        # 2. Extract VirtualFile reference
        virtual_file = getattr(selected_item, "file_object", selected_item)

        # 3. Launch Text Editor via Runtime / Desktop App Manager
        # References desktop/shell/desktop.py or runtime/app_manager.py
        editor_instance = self.desktop.app_manager.launch_app("text_editor") # or "Text Editor"
        
        # 4. Pass the VirtualFile object directly into the editor
        if editor_instance:
            editor_instance.open_virtual_file(virtual_file)
            self.desktop.window_manager.bring_to_front(editor_instance)