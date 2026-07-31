class ExplorerState:

    def __init__(self):

        # navigation
        self.current_folder = None
        self.history = [None]
        self.history_index = 0

        # selection
        self.selected_item = None
        self.clipboard_item = None

        # sidebar
        self.selected_sidebar = "Computer"

        # clicks
        self.last_click_time = 0
        self.last_clicked = None
        self.double_click_time = 0.30

        # UI
        self.search_progress = 0.0

        # window
        self.minimized = False
        self.closed = False
        self.is_active = False