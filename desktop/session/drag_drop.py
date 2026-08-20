
import pygame

class DragDropService:
    """Service for handling drag and drop operations"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.dragging = False
        self.drag_data = None
        self.drag_source = None
        self.drag_target = None
        self.ghost_surface = None
        self.offset_x = 0
        self.offset_y = 0

    def start_drag(self, source, data, ghost_surface=None):
        """Start a drag operation"""
        self.dragging = True
        self.drag_source = source
        self.drag_data = data
        self.ghost_surface = ghost_surface

        mx, my = pygame.mouse.get_pos()
        if ghost_surface:
            self.offset_x = ghost_surface.get_width() // 2
            self.offset_y = ghost_surface.get_height() // 2
        else:
            self.offset_x = 0
            self.offset_y = 0

        print(f"[VOS] Drag started: {data}")

    def update_drag(self):
        """Update drag position"""
        if not self.dragging:
            return

        mx, my = pygame.mouse.get_pos()

        self.drag_target = self._find_target(mx, my)

    def end_drag(self, cancel=False):
        """End the drag operation"""
        if not self.dragging:
            return

        if cancel:
            print("[VOS] Drag cancelled")
        elif self.drag_target:

            self._perform_drop()
            print("[VOS] Drag dropped")
        else:
            print("[VOS] Drag ended")

        self.dragging = False
        self.drag_data = None
        self.drag_source = None
        self.drag_target = None
        self.ghost_surface = None

    def _find_target(self, x, y):
        """Find the target for a drop"""

        return None

    def _perform_drop(self):
        """Execute the drop operation"""

        if self.drag_source and self.drag_target:

            if isinstance(self.drag_data, dict):
                if self.drag_data.get('type') == 'file':

                    self._handle_file_drop()
                elif self.drag_data.get('type') == 'folder':

                    self._handle_folder_drop()
                elif self.drag_data.get('type') == 'text':

                    self._handle_text_drop()

    def _handle_file_drop(self):
        """Handle dropping a file"""
        print(f"[VOS] File dropped: {self.drag_data.get('name')}")

    def _handle_folder_drop(self):
        """Handle dropping a folder"""
        print(f"[VOS] Folder dropped: {self.drag_data.get('name')}")

    def _handle_text_drop(self):
        """Handle dropping text"""
        print(f"[VOS] Text dropped: {self.drag_data.get('content')}")

    def draw_ghost(self, surface):
        """Draw the ghost image during drag"""
        if not self.dragging or not self.ghost_surface:
            return

        mx, my = pygame.mouse.get_pos()
        ghost_rect = self.ghost_surface.get_rect(center=(mx, my))
        surface.blit(self.ghost_surface, ghost_rect)
