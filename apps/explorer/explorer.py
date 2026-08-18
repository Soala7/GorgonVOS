from apps.explorer.explorer_window import ExplorerWindow

class Explorer:

    def __init__(self, window_manager):
        self.window_manager = window_manager

        self.window = ExplorerWindow(
            window_manager=self.window_manager
        )

    def open(self):
        """Open the Explorer window."""
        self.window.closed = False
        self.window.minimized = False
        self.window.activate()

        if self.window_manager:
            if self.window not in self.window_manager.windows:
                self.window_manager.add_window(self.window)
            else:
                self.window_manager.focus_window(self.window)

    def close(self):
        """Close the Explorer window."""
        self.window.closed = True
        self.window.deactivate()

    def minimize(self):
        """Minimize the Explorer window."""
        self.window.minimized = True
        self.window.deactivate()

    def activate(self):
        self.window.activate()

    def deactivate(self):
        self.window.deactivate()

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