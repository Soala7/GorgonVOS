
"""Navigation logic for Explorer"""

class ExplorerNavigation:

    def navigate_to(self, folder):

        target_name = getattr(folder, "name", "Computer (Dashboard)")
        print(f"[VOS] Navigating to: {target_name}")

        self.current_folder = folder

        self.history = self.history[:self.history_index + 1]

        if folder is not None:
            self.history.append(folder)
            self.history_index += 1

        self._sync_sidebar_from_current_folder()
        self.selected_item = None

        if folder is not None:
            self.title = f"{target_name} - Explorer"
        else:
            self.title = "Explorer"

        print(f"[VOS] History length: {len(self.history)}")

    def _sync_sidebar_from_current_folder(self):
        """Automatically updates sidebar highlight based on current location"""
        if self.current_folder is None:
            self.selected_sidebar = "Computer"
            return

        curr = self.current_folder
        while curr is not None:
            name = getattr(curr, "name", None)
            if name in [item[0] for item in self.sidebar_items]:
                self.selected_sidebar = name
                return
            curr = getattr(curr, "parent", None)

    def go_back(self):
        if self.history_index <= 0:
            print("[VOS] Cannot go back, at start of history.")
            return
        self.history_index -= 1
        self.current_folder = self.history[self.history_index]
        print(f"[VOS] Navigating BACK to: {getattr(self.current_folder, 'name', 'Computer')}")
        self._sync_sidebar_from_current_folder()
        self.selected_item = None

    def go_forward(self):
        if self.history_index >= len(self.history) - 1:
            print("[VOS] Cannot go forward, at end of history.")
            return
        self.history_index += 1
        self.current_folder = self.history[self.history_index]
        print(f"[VOS] Navigating FORWARD to: {getattr(self.current_folder, 'name', 'Computer')}")
        self._sync_sidebar_from_current_folder()
        self.selected_item = None

    def go_up(self):
        if self.current_folder is None:
            print("[VOS] Cannot go up, already at Computer root.")
            return
        parent = getattr(self.current_folder, "parent", None)
        if parent is None:
            print("[VOS] Parent is None, navigating to Computer root.")
            self.navigate_to(None)
            return

        print(f"[VOS] Navigating UP to: {getattr(parent, 'name', 'Unknown')}")
        self.current_folder = parent
        self.history_index += 1
        self.history = self.history[:self.history_index]
        self.history.append(parent)
        self._sync_sidebar_from_current_folder()
        self.selected_item = None

    def get_breadcrumb_path(self) -> list[str]:
        """Get breadcrumb trail"""
        path = ["Computer"]
        curr = self.current_folder
        parts = []
        while curr is not None:
            parts.insert(0, getattr(curr, "name", "Folder"))
            curr = getattr(curr, "parent", None)
        return path + parts

    def refresh_view(self):
        """Refresh the current view"""
        current = self.current_folder
        self.current_folder = None
        self.current_folder = current
        print("[VOS] View refreshed")
