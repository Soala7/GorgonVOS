# apps/explorer/explorer_window.py
from __future__ import annotations

import time
import pygame

from desktop.ui.window.window import Window
from desktop.assests.icon_manager import IconManager
from bridge.vos_api import vos_api

# Import mixins
from apps.explorer.explorer_navigation import ExplorerNavigation
from apps.explorer.explorer_operations import ExplorerOperations
from apps.explorer.explorer_render import ExplorerRender

class ExplorerWindow(ExplorerNavigation, ExplorerOperations, ExplorerRender, Window):
    """Main Explorer Window with navigation, operations, and rendering"""
    
    TITLEBAR_HEIGHT = 40

    def __init__(self, title="Explorer", width=800, height=600, name="Explorer"):
        # Initialize Window first
        super().__init__(title, width, height, name)
        
        # Initialize filesystem
        self._init_filesystem()
        
        # Window state
        self.minimized = False
        self.closed = False
        self.is_active = False
        self.transform.position.x = 180
        self.transform.position.y = 80
        
        # User settings
        self.selected_sidebar = "Computer"
        self.user_name = self._get_username()
        self.search_progress = 0.0
        
        # Navigation state
        self.current_folder = None
        self.history = []
        self.history_index = 0
        
        # Selection state
        self.selected_item = None
        self.item_rects = []
        self.sidebar_hitboxes = []
        self.center_hitboxes = []
        
        # Double-click handling
        self.double_click_time = 0.60
        self.last_click_time = time.time()  # Initialize with current time
        self.last_clicked = None
        
        # Sidebar items
        self.sidebar_items = [
            ("Computer", "explorer/computer"),
            ("Documents", "explorer/documents"),
            ("Downloads", "explorer/downloads"),
            ("Pictures", "explorer/photo"),
            ("Videos", "explorer/videos"),
            ("Music", "explorer/musics"),
            ("Storage", "explorer/storages"),
            ("Trash", "explorer/trashs"),
        ]
        
        # Load icons
        self._load_icons()
        
        # Navigate to root
        # Navigate to Computer (dashboard view)
        self.navigate_to(None)  # None = Computer dashboard
        
        print("[VOS] ExplorerWindow initialized.")

    def _init_filesystem(self):
        """Initialize filesystem connection"""
        self.filesystem = None
        if hasattr(vos_api, "filesystem") and vos_api.filesystem is not None:
            self.filesystem = vos_api.filesystem
        else:
            try:
                from filesystem.filesystem import FileSystem
                self.filesystem = FileSystem()
                vos_api.filesystem = self.filesystem
            except Exception as e:
                print(f"[ERROR] Could not initialize filesystem: {e}")
                self.filesystem = None

    def _get_username(self):
        """Get current username"""
        try:
            from desktop.session.session import get_current_user
            user = get_current_user()
            if user:
                return user.get('name', 'User')
        except:
            pass
        return "User"

    def _load_icons(self):
        """Load all icons with proper folder icons"""
        self.raw_icons = {
            "search": IconManager.get("explorer/search", 48),
            "plus": IconManager.get("explorer/plus", 64),
            "chatgpt": IconManager.get("explorer/chatgpt", 48),
            "back": IconManager.get("explorer/back", 48),
            "forward": IconManager.get("explorer/forward", 48),
            "down": IconManager.get("explorer/down", 48),
            "wifi": IconManager.get("explorer/wifi", 48),
            "bell": IconManager.get("explorer/notification", 48),  # This is already here but might be missing file
            "user": IconManager.get("explorer/user", 48),
            "document": IconManager.get("explorer/document", 48),
            "folder": IconManager.get("explorer/folder", 48),
            # Folder icons for sidebar
            "computer": IconManager.get("explorer/computer", 48),
            "documents_folder": IconManager.get("explorer/documents_folder", 48),
            "downloads_folder": IconManager.get("explorer/downloads_folder", 48),
            "images_folder": IconManager.get("explorer/images_folder", 48),
            "videos_folder": IconManager.get("explorer/videos_folder", 48),
            "musics_folder": IconManager.get("explorer/musics_folder", 48),
            "storages": IconManager.get("explorer/storages", 48),
            "trashs": IconManager.get("explorer/trashs", 48),
            # File type icons
            "python": IconManager.get("files/python", 48),
            "text": IconManager.get("files/text", 48),
            "json": IconManager.get("files/json", 48),
            "html": IconManager.get("files/html", 48),
            "css": IconManager.get("files/css", 48),
            "javascript": IconManager.get("files/javascript", 48),
            "image": IconManager.get("files/image", 48),
            "music": IconManager.get("files/music", 48),
            "video": IconManager.get("files/video", 48),
            "pdf": IconManager.get("files/pdf", 48),
            "spreadsheet": IconManager.get("files/spreadsheet", 48),
            "zip": IconManager.get("files/zip", 48),
            # Center strip icons - Map to actual icon files
            "center_1": IconManager.get("explorer/documents_folder", 48),  # Documents
            "center_2": IconManager.get("explorer/downloads_folder", 48),  # Downloads
            "center_3": IconManager.get("explorer/favorite_folder", 48),  # Favorites
            "center_4": IconManager.get("explorer/videos_folder", 48),    # Videos
            "center_5": IconManager.get("explorer/images_folder", 48),    # Pictures
            "center_6": IconManager.get("explorer/musics_folder", 48),    # Music
        }
        
        # Load sidebar icons
        for name, path in self.sidebar_items:
            self.raw_icons[name] = IconManager.get(path, 48)
    def _get_scaled_icon(self, key: str, target_size: int) -> pygame.Surface | None:
        """Get scaled icon"""
        # Check if we have this icon in raw_icons
        raw = self.raw_icons.get(key)
        
        # Debug: print what we found
        #print(f"[VOS] _get_scaled_icon: key='{key}', raw_type={type(raw) if raw else 'None'}")
        
        if raw is not None:
            try:
                if isinstance(raw, pygame.Surface):
                    return pygame.transform.smoothscale(raw, (target_size, target_size))
                # If it's a string path, try to load it
                elif isinstance(raw, str):
                    import os
                    if os.path.exists(raw):
                        img = pygame.image.load(raw)
                        if img:
                            return pygame.transform.smoothscale(img, (target_size, target_size))
            except Exception as e:
                print(f"[VOS] Error scaling icon '{key}': {e}")
        
        # ... rest of the method ...
        
        # Try alternative keys
        alt_key_map = {
            "documents_folder": ["documents", "Documents"],
            "downloads_folder": ["downloads", "Downloads"],
            "images_folder": ["images", "Pictures", "photo"],
            "videos_folder": ["videos", "Videos"],
            "musics_folder": ["musics", "Music"],
            "computer": ["Computer"],
            "storages": ["Storage"],
            "trashs": ["Trash"],
        }
        
        if key in alt_key_map:
            for alt_key in alt_key_map[key]:
                alt_raw = self.raw_icons.get(alt_key)
                if alt_raw is not None:
                    try:
                        if isinstance(alt_raw, pygame.Surface):
                            return pygame.transform.smoothscale(alt_raw, (target_size, target_size))
                    except:
                        pass
        
        # Try direct file loading as last resort
        import os
        possible_paths = [
            f"assets/icons/explorer/{key}.png",
            f"assets/icons/explorer/{key}.svg",
            f"assets/icons/explorer/{key}.PNG",
        ]
        # Also try without "_folder" suffix
        if key.endswith("_folder"):
            base = key[:-7]  # Remove "_folder"
            possible_paths.extend([
                f"assets/icons/explorer/{base}.png",
                f"assets/icons/explorer/{base}.svg",
                f"assets/icons/explorer/{base}.PNG",
            ])
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path)
                    if img:
                        # Cache it
                        self.raw_icons[key] = img
                        return pygame.transform.smoothscale(img, (target_size, target_size))
                except:
                    pass
        
        print(f"[VOS] Could not load icon: {key}")
        return None

    def _get_folder_items(self, folder) -> list:
        """Extract items from folder"""
        if folder is None:
            return []
        
        items = []
        
        # Get folders
        if hasattr(folder, 'folders'):
            folders_attr = folder.folders
            if isinstance(folders_attr, dict):
                items.extend(folders_attr.values())
            elif isinstance(folders_attr, list):
                items.extend(folders_attr)
        
        # Get files
        if hasattr(folder, 'files'):
            files_attr = folder.files
            if isinstance(files_attr, dict):
                for filename, content in files_attr.items():
                    file_obj = type('VOSFile', (object,), {
                        'name': filename,
                        'content': content,
                        'is_folder': False,
                        'path': f"{getattr(folder, 'path', '/')}/{filename}"
                    })()
                    items.append(file_obj)
            elif isinstance(files_attr, list):
                items.extend(files_attr)
        
        return items

    def _is_item_folder(self, item) -> bool:
        """Check if item is a folder"""
        if hasattr(item, "is_folder"):
            return item.is_folder
        if hasattr(item, "folders") or hasattr(item, "files"):
            return True
        return False

    # ==================== Lifecycle Methods ====================
    
    def activate(self):
        print("[VOS] ExplorerWindow activated.")
        super().activate()
        self.is_active = True

    def deactivate(self):
        print("[VOS] ExplorerWindow deactivated.")
        super().deactivate()
        self.is_active = False

    def update(self, dt):
        if dt is None:
            dt = 0.016

        mx, my = pygame.mouse.get_pos()
        wx, wy = self.transform.position.x, self.transform.position.y
        rel_x, rel_y = mx - wx, my - wy
        ww, wh = self.transform.size.width, self.transform.size.height

        scale = max(0.65, min(ww / 920.0, wh / 620.0))
        content_x = self._get_content_x(ww, scale)
        base_search_w = min(int(260 * scale), int((ww - content_x) * 0.60))
        base_search_h = max(28, int(36 * scale))
        base_search_rect = pygame.Rect(content_x, self.TITLEBAR_HEIGHT + 10, base_search_w, base_search_h)

        is_hovered = base_search_rect.collidepoint(rel_x, rel_y)
        target = 1.0 if is_hovered else 0.0
        
        self.search_progress += (target - self.search_progress) * min(1.0, 3.0 * dt)

    def _get_content_x(self, ww, scale):
        """Calculate content x position"""
        left_w = max(145, int(ww * 0.185))
        center_w = max(48, int(ww * 0.065))
        return 16 + left_w + 10 + center_w + 24

    # ==================== Event Handling ====================
    
    def handle_event(self, event):
        mx, my = pygame.mouse.get_pos()
        rel_x = mx - self.transform.position.x
        rel_y = my - self.transform.position.y
        ww, wh = self.transform.size.width, self.transform.size.height

        if hasattr(event, "type"):
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"[VOS] MOUSEBUTTONDOWN: button={event.button}, pos={event.pos}")
            elif event.type == pygame.MOUSEBUTTONUP:
                print(f"[VOS] MOUSEBUTTONUP: button={event.button}")

        scale = max(0.65, min(ww / 920.0, wh / 620.0))

        is_click = False
        if hasattr(event, "type") and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            is_click = True
        elif type(event).__name__ in ("MousePressEvent", "MouseClickEvent"):
            is_click = True

        if is_click:
            self._handle_click(rel_x, rel_y, scale, ww, wh)

        super().handle_event(event)

    def _handle_click(self, rel_x, rel_y, scale, ww, wh):
        """Handle mouse click events"""
        # Title bar navigation buttons
        if rel_y <= self.TITLEBAR_HEIGHT:
            self._handle_titlebar_click(rel_x, rel_y, scale)
            return
        
        # Main content clicks
        if rel_y > self.TITLEBAR_HEIGHT:
            self._handle_content_click(rel_x, rel_y, scale, ww, wh)

    def _handle_titlebar_click(self, rel_x, rel_y, scale):
        """Handle clicks on titlebar buttons"""
        nav_x = int(18 * scale)
        top_icon_sz = max(12, int(16 * scale))
        
        # Back button
        if pygame.Rect(nav_x, (self.TITLEBAR_HEIGHT - top_icon_sz)//2, top_icon_sz, top_icon_sz).collidepoint(rel_x, rel_y):
            print("[VOS] Clicked: Back")
            self.go_back()
            return
        nav_x += int(24 * scale)
        
        # Forward button
        if pygame.Rect(nav_x, (self.TITLEBAR_HEIGHT - top_icon_sz)//2, top_icon_sz, top_icon_sz).collidepoint(rel_x, rel_y):
            print("[VOS] Clicked: Forward")
            self.go_forward()
            return
        nav_x += int(24 * scale)
        
        # Up button
        if pygame.Rect(nav_x, (self.TITLEBAR_HEIGHT - top_icon_sz)//2, top_icon_sz, top_icon_sz).collidepoint(rel_x, rel_y):
            print("[VOS] Clicked: Up")
            self.go_up()
            return

    def _handle_content_click(self, rel_x, rel_y, scale, ww, wh):
        """Handle clicks on main content area"""
        bottom_margin = int(20 * scale)
        left_w = max(145, int(ww * 0.185))
        center_w = max(48, int(ww * 0.065))
        
        left_panel_rect = pygame.Rect(16, self.TITLEBAR_HEIGHT + 10, left_w, 
                                     wh - self.TITLEBAR_HEIGHT - bottom_margin - 10)
        center_strip_rect = pygame.Rect(left_panel_rect.right + 10, self.TITLEBAR_HEIGHT + 10, 
                                       center_w, wh - self.TITLEBAR_HEIGHT - bottom_margin - 10)

        # Check sidebar clicks
        if left_panel_rect.collidepoint(rel_x, rel_y):
            self._handle_sidebar_click(rel_x, rel_y, left_panel_rect, scale)
            return
        
        # Check center strip clicks
        if center_strip_rect.collidepoint(rel_x, rel_y):
            self._handle_center_strip_click(rel_x, rel_y, center_strip_rect, scale)
            return
        
        # Check folder content clicks
        if self.current_folder is not None:
            self._handle_folder_item_click(rel_x, rel_y, scale)
            return
        
        # Clicked empty space
        self.selected_item = None

    def _handle_sidebar_click(self, rel_x, rel_y, panel_rect, scale):
        """Handle clicks on sidebar items"""
        y = panel_rect.y + int(10 * scale)
        item_h = max(24, int(panel_rect.height * 0.054))
        
        for name, path in self.sidebar_items:
            item_rect = pygame.Rect(panel_rect.x + 6, y, panel_rect.width - 12, item_h)
            if item_rect.collidepoint(rel_x, rel_y):
                #print(f"[VOS] Sidebar clicked: '{name}' -> '{path}'")
                self.selected_sidebar = name
                
                if name == "Computer":
                    self.navigate_to(None)
                elif self.filesystem and hasattr(self.filesystem, "get_special_folder"):
                    folder = self.filesystem.get_special_folder(path)
                    if folder:
                        self.navigate_to(folder)
                    else:
                        print(f"[VOS] Could not find special folder: {path}")
                return
            y += item_h + int(2 * scale)

    # Add to ExplorerWindow class
    '''def _handle_mouse_drag(self, event):
        """Handle mouse drag events for drag and drop"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicking on an item
            for rect, item in self.item_rects:
                if rect.collidepoint(event.pos):
                    # Start drag
                    from desktop.services.drag_drop import DragDropService
                    drag = DragDropService()
                    
                    # Create ghost surface
                    ghost = self._create_ghost_image(item)
                    
                    # Start drag
                    drag.start_drag(
                        source=self,
                        data={
                            'type': 'file' if not self._is_item_folder(item) else 'folder',
                            'name': getattr(item, 'name', 'Unknown'),
                            'item': item
                        },
                        ghost_surface=ghost
                    )
                    return True
        return False

    def _create_ghost_image(self, item):
        """Create a ghost image for drag feedback"""
        item_name = getattr(item, 'name', 'Unknown')
        is_folder = self._is_item_folder(item)
        
        # Create ghost surface
        ghost = pygame.Surface((100, 40), pygame.SRCALPHA)
        pygame.draw.rect(ghost, (255, 255, 255, 200), (0, 0, 100, 40), border_radius=8)
        pygame.draw.rect(ghost, (200, 200, 200, 100), (0, 0, 100, 40), border_radius=8, width=2)
        
        # Add icon
        icon_size = 24
        if is_folder:
            icon = self._get_scaled_icon("folder", icon_size)
        else:
            icon = self._get_file_icon(item_name, icon_size)
        
        if icon:
            ghost.blit(icon, (8, 8))
        
        # Add name
        font = pygame.font.SysFont("Segoe UI", 11)
        text = font.render(item_name[:15], True, (50, 50, 55))
        ghost.blit(text, (40, 12))
        
        return ghost'''

    def _handle_center_strip_click(self, rel_x, rel_y, strip_rect, scale):
        """Handle clicks on center strip items"""
        ring_size = int(36 * scale)
        y = strip_rect.y + int(10 * scale)
        spacing_y = int(40 * scale)
        
        center_mapping = [
            ("Documents", "explorer/documents"),
            ("Downloads", "explorer/downloads"),
            ("Pictures", "explorer/photo"),
            ("Videos", "explorer/videos"),
            ("Music", "explorer/musics")
        ]
        
        for key_name, path in center_mapping:
            base_ring_rect = pygame.Rect(strip_rect.centerx - ring_size//2, y, ring_size, ring_size)
            if base_ring_rect.collidepoint(rel_x, rel_y):
                #print(f"[VOS] Center strip clicked: '{key_name}' -> '{path}'")
                self.selected_sidebar = key_name
                
                if self.filesystem and hasattr(self.filesystem, "get_special_folder"):
                    folder = self.filesystem.get_special_folder(path)
                    if folder:
                        self.navigate_to(folder)
                    else:
                        print(f"[VOS] Could not find: {path}")
                return
            y += spacing_y

    # apps/explorer/explorer_window.py

    def _on_file_double_click(self, selected_item):
        """Triggered when an item in the file view is double-clicked."""
        
        # 1. Ensure the item is a file (not a directory)
        if getattr(selected_item, "is_directory", False):
            self.navigate_to(selected_item.path)
            return

        # 2. Extract the VirtualFile instance
        virtual_file = getattr(selected_item, "file_object", selected_item)

        # 3. Check for supported text formats
        file_name = getattr(virtual_file, "name", "")
        if file_name.endswith((".txt", ".md", ".py", ".json", ".csv", ".log")) or not "." in file_name:
            
            # Launch or retrieve an Editor instance via Desktop / AppLauncher
            editor_window = self.desktop.launch_app("Text Editor")
            
            # Pass the VirtualFile to open_virtual_file()
            if editor_window:
                editor_window.open_virtual_file(virtual_file)
                self.desktop.window_manager.focus_window(editor_window)

    def _handle_folder_item_click(self, rel_x, rel_y, scale):
        """Handle clicks on folder items (single/double click)"""
        clicked_item = None
        for rect, child in self.item_rects:
            if rect.collidepoint(rel_x, rel_y):
                clicked_item = child
                break

        if clicked_item is not None:
            item_name = getattr(clicked_item, "name", "Unknown")
            now = time.time()
            
            # Check if this is a double click
            is_double_click = False
            if self.last_clicked is not None:
                last_name = getattr(self.last_clicked, 'name', '')
                delta = now - self.last_click_time
                is_double_click = (last_name == item_name and delta < self.double_click_time)
                
                print(f"[VOS] Click: '{item_name}' | Last: '{last_name}' | Delta: {delta:.3f}s | Double: {is_double_click}")
            
            if is_double_click:
                print(f"[VOS] >>> DOUBLE-CLICK DETECTED! <<<")
                if self._is_item_folder(clicked_item):
                    self.navigate_to(clicked_item)
                else:
                    self.open_item(clicked_item)
                # Reset after double click
                self.last_clicked = None
                self.last_click_time = 0.0
            else:
                print(f"[VOS] SINGLE-CLICK: '{item_name}'")
                self.selected_item = clicked_item
                # Store for next click
                self.last_clicked = clicked_item
                self.last_click_time = now
        else:
            # Clicked empty space
            self.selected_item = None
            self.last_clicked = None
            self.last_click_time = 0.0

















            