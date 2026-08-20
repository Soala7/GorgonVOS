class ExplorerState:

    def __init__(self):

        self.current_folder = None
        self.history = [None]
        self.history_index = 0

        self.selected_item = None
        self.clipboard_item = None

        self.selected_sidebar = "Computer"

        self.last_click_time = 0
        self.last_clicked = None
        self.double_click_time = 0.30

        self.search_progress = 0.0

        self.minimized = False
        self.closed = False
        self.is_active = False
