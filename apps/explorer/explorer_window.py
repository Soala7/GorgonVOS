from __future__ import annotations

import os
import time
import pygame

from desktop.ui.window.window import Window
from desktop.assests.icon_manager import IconManager
from bridge.vos_api import vos_api

from apps.explorer.explorer_navigation import ExplorerNavigation
from apps.explorer.explorer_operations import ExplorerOperations
from apps.explorer.explorer_render import ExplorerRender


class ExplorerWindow(ExplorerNavigation, ExplorerOperations, ExplorerRender, Window):
    """Main Explorer Window handling navigation, file operations, and rendering."""

    TITLEBAR_HEIGHT = 40

    def __init__(self, window_manager, title="Explorer", width=800, height=600, name="Explorer"):
        super().__init__(title, width, height, name)
        self.window_manager = window_manager
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

        # Drag & Drop state
        self.dragging_item = None
        self.dragging = False
        self.drag_start_pos = (0, 0)
        self.drag_threshold = 8
        self.drop_target = None

        # Folder creation
        self.new_folder_counter = 1

        # Double-click handling
        self.double_click_time = 0.60
        self.last_click_time = time.time()
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

        self._load_icons()
        self.navigate_to(None)  # None = Computer dashboard

    def _init_filesystem(self):
        self.filesystem = None
        if hasattr(vos_api, "filesystem") and vos_api.filesystem is not None:
            self.filesystem = vos_api.filesystem
        else:
            try:
                from filesystem.filesystem import FileSystem
                self.filesystem = FileSystem()
                vos_api.filesystem = self.filesystem
            except Exception:
                self.filesystem = None

    def _get_username(self):
        try:
            from desktop.session.session import get_current_user
            user = get_current_user()
            if user:
                return user.get("name", "User")
        except Exception:
            pass
        return "User"

    def _load_icons(self):
        size = 48
        self.raw_icons = {
            "search": IconManager.get("explorer/search", size),
            "plus": IconManager.get("explorer/plus", 64),
            "chatgpt": IconManager.get("explorer/chatgpt", size),
            "back": IconManager.get("explorer/back", size),
            "forward": IconManager.get("explorer/forward", size),
            "down": IconManager.get("explorer/down", size),
            "wifi": IconManager.get("explorer/wifi", size),
            "bell": IconManager.get("explorer/notification", size),
            "user": IconManager.get("explorer/user", size),
            "document": IconManager.get("explorer/document", size),
            "folder": IconManager.get("explorer/folder", size),
            # Sidebar folder icons
            "computer": IconManager.get("explorer/computer", size),
            "documents_folder": IconManager.get("explorer/documents_folder", size),
            "downloads_folder": IconManager.get("explorer/downloads_folder", size),
            "images_folder": IconManager.get("explorer/images_folder", size),
            "videos_folder": IconManager.get("explorer/videos_folder", size),
            "musics_folder": IconManager.get("explorer/musics_folder", size),
            "storages": IconManager.get("explorer/storages", size),
            "trashs": IconManager.get("explorer/trashs", size),
            # File type icons
            "python": IconManager.get("files/python", size),
            "text": IconManager.get("files/text", size),
            "json": IconManager.get("files/json", size),
            "html": IconManager.get("files/html", size),
            "css": IconManager.get("files/css", size),
            "javascript": IconManager.get("files/javascript", size),
            "image": IconManager.get("files/image", size),
            "music": IconManager.get("files/music", size),
            "video": IconManager.get("files/video", size),
            "pdf": IconManager.get("files/pdf", size),
            "spreadsheet": IconManager.get("files/spreadsheet", size),
            "zip": IconManager.get("files/zip", size),
            # Center strip shortcuts
            "center_1": IconManager.get("explorer/documents_folder", size),
            "center_2": IconManager.get("explorer/downloads_folder", size),
            "center_3": IconManager.get("explorer/favorite_folder", size),
            "center_4": IconManager.get("explorer/videos_folder", size),
            "center_5": IconManager.get("explorer/images_folder", size),
            "center_6": IconManager.get("explorer/musics_folder", size),
        }

        for name, path in self.sidebar_items:
            self.raw_icons[name] = IconManager.get(path, size)

    def _get_scaled_icon(self, key: str, target_size: int) -> pygame.Surface | None:
        raw = self.raw_icons.get(key)
        if raw is not None:
            try:
                if isinstance(raw, pygame.Surface):
                    return pygame.transform.smoothscale(raw, (target_size, target_size))
                elif isinstance(raw, str) and os.path.exists(raw):
                    img = pygame.image.load(raw)
                    if img:
                        return pygame.transform.smoothscale(img, (target_size, target_size))
            except Exception:
                pass

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
                if isinstance(alt_raw, pygame.Surface):
                    try:
                        return pygame.transform.smoothscale(alt_raw, (target_size, target_size))
                    except Exception:
                        pass

        possible_paths = [
            f"assets/icons/explorer/{key}.png",
            f"assets/icons/explorer/{key}.svg",
            f"assets/icons/explorer/{key}.PNG",
        ]
        if key.endswith("_folder"):
            base = key[:-7]
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
                        self.raw_icons[key] = img
                        return pygame.transform.smoothscale(img, (target_size, target_size))
                except Exception:
                    pass

        return None

    def _get_folder_items(self, folder) -> list:
        if folder is None:
            return []

        items = []
        if hasattr(folder, "folders"):
            folders_attr = folder.folders
            if isinstance(folders_attr, dict):
                items.extend(folders_attr.values())
            elif isinstance(folders_attr, list):
                items.extend(folders_attr)

        if hasattr(folder, "files"):
            files_attr = folder.files
            if isinstance(files_attr, dict):
                for filename, content in files_attr.items():
                    clean_path = f"{getattr(folder, 'path', '/')}/{filename}".replace("//", "/")
                    file_obj = type("VOSFile", (object,), {
                        "name": filename,
                        "content": content,
                        "is_folder": False,
                        "parent": folder,
                        "path": clean_path
                    })()
                    items.append(file_obj)
            elif isinstance(files_attr, list):
                items.extend(files_attr)

        return items

    def _is_item_folder(self, item) -> bool:
        if hasattr(item, "is_folder"):
            return item.is_folder
        return hasattr(item, "folders") or hasattr(item, "files")

    def activate(self):
        super().activate()
        self.is_active = True

    def deactivate(self):
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
        left_w = max(145, int(ww * 0.185))
        center_w = max(48, int(ww * 0.065))
        return 16 + left_w + 10 + center_w + 24

    def handle_event(self, event):
        """
        Handle Explorer input:
        - Click/select
        - Double click/open
        - Delete key
        - Drag and drop
        """
        ev_type = getattr(event, "type", None)
        ev_key = getattr(event, "key", None)

        # --------------------------------------------------
        # Keyboard Event Interception
        # --------------------------------------------------
        is_key_down = (
            ev_type == pygame.KEYDOWN or 
            type(event).__name__ in ("KeyPressEvent", "KeyDownEvent", "KeyEvent")
        )

        if is_key_down and ev_key is not None:
            if ev_key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                if self.selected_item is not None:
                    target = self.selected_item
                    success = False

                    if hasattr(self, "delete_item"):
                        success = self.delete_item(target)

                    if not success and self.current_folder is not None:
                        item_name = getattr(target, "name", None)
                        if item_name:
                            if hasattr(self.current_folder, "files") and isinstance(self.current_folder.files, dict):
                                if item_name in self.current_folder.files:
                                    del self.current_folder.files[item_name]
                                    success = True
                            if not success and hasattr(self.current_folder, "folders") and isinstance(self.current_folder.folders, dict):
                                if item_name in self.current_folder.folders:
                                    del self.current_folder.folders[item_name]
                                    success = True

                    if success:
                        self.selected_item = None
                        self._save_filesystem()
                        self._refresh_current_folder()

                return

            if ev_key == pygame.K_n:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
                    self._create_folder()
                    return

        # --------------------------------------------------
        # Convert Mouse Coordinates to Window-Relative
        # --------------------------------------------------
        mx, my = pygame.mouse.get_pos()
        rel_x = mx - self.transform.position.x
        rel_y = my - self.transform.position.y
        rel_pos = (rel_x, rel_y)

        if ev_type is not None:
            if ev_type == pygame.MOUSEBUTTONDOWN and getattr(event, "button", None) == 1:
                self._begin_drag(rel_pos)

            elif ev_type == pygame.MOUSEMOTION:
                self._update_drag(rel_pos)

            elif ev_type == pygame.MOUSEBUTTONUP and getattr(event, "button", None) == 1:
                self._finish_drag(rel_pos)

        # --------------------------------------------------
        # Standard Click Dispatching
        # --------------------------------------------------
        ww = self.transform.size.width
        wh = self.transform.size.height
        scale = max(0.65, min(ww / 920.0, wh / 620.0))

        is_click = (
            ev_type == pygame.MOUSEBUTTONDOWN and getattr(event, "button", None) == 1
        ) or type(event).__name__ in ("MousePressEvent", "MouseClickEvent")

        if is_click and not self.dragging:
            self._handle_click(rel_x, rel_y, scale, ww, wh)

        super().handle_event(event)

    def _begin_drag(self, rel_pos):
        """Begin potential drag using relative window positions."""
        if self.current_folder is None:
            return

        clicked_item = None
        for rect, item in self.item_rects:
            if rect.collidepoint(rel_pos):
                clicked_item = item
                break

        if clicked_item is None:
            return

        self.selected_item = clicked_item
        self.dragging_item = clicked_item
        self.drag_start_pos = rel_pos
        self.dragging = False
        self.drop_target = None

    def _update_drag(self, rel_pos):
        """Update drag progress and detect folder drop target under cursor."""
        if self.dragging_item is None:
            return

        start_x, start_y = self.drag_start_pos
        current_x, current_y = rel_pos

        distance = ((current_x - start_x) ** 2 + (current_y - start_y) ** 2) ** 0.5

        if not self.dragging and distance >= self.drag_threshold:
            self.dragging = True

        if not self.dragging:
            return

        self.drop_target = None

        # Find folder underneath relative cursor position
        for rect, item in self.item_rects:
            if not rect.collidepoint(rel_pos):
                continue
            if not self._is_item_folder(item):
                continue
            if self._is_computer_item(item):
                continue
            if item is self.dragging_item:
                continue

            self.drop_target = item
            break

    def _finish_drag(self, rel_pos):
        """Complete drag operation and move file to target directory."""
        if self.dragging_item is None:
            return

        dragged_item = self.dragging_item
        target_folder = self.drop_target
        was_dragging = self.dragging

        self.dragging_item = None
        self.dragging = False
        self.drop_target = None

        if not was_dragging or target_folder is None or dragged_item is target_folder:
            return

        self._move_item_to_folder(dragged_item, target_folder)

    def _create_folder(self):
        """
        Create a new folder inside the currently opened directory.
        """

        if self.current_folder is None:
            print("[VOS] Cannot create folder from Computer view.")
            return False

        while True:
            folder_name = f"New Folder {self.new_folder_counter}"

            exists = False

            if hasattr(self.current_folder, "folders"):
                folders = self.current_folder.folders

                if isinstance(folders, dict):
                    exists = folder_name in folders

            if not exists:
                break

            self.new_folder_counter += 1

        success = self.create_new_folder(folder_name)

        if success:
            self.new_folder_counter += 1

            self._refresh_current_folder()

            print(
                f"[VOS] Created folder: {folder_name}"
            )

        return success

    def _refresh_current_folder(self):
        """
        Refresh the current Explorer view after
        creating, deleting, or moving an item.
        """

        if self.current_folder is None:
            self.navigate_to(None)
            return

        current = self.current_folder
        self.item_rects = []

        # Re-navigate to force the renderer/navigation
        # to rebuild the visible item list.
        self.navigate_to(current)

    def _handle_click(self, rel_x, rel_y, scale, ww, wh):
        """Dispatch click actions based on region hitboxes."""
        if rel_y <= self.TITLEBAR_HEIGHT:
            self._handle_titlebar_click(rel_x, rel_y, scale)
        else:
            self._handle_content_click(rel_x, rel_y, scale, ww, wh)

    def _handle_titlebar_click(self, rel_x, rel_y, scale):
        """Handle titlebar navigation controls (back, forward, up)."""
        nav_x = int(18 * scale)
        top_icon_sz = max(12, int(16 * scale))

        # Back button
        if pygame.Rect(nav_x, (self.TITLEBAR_HEIGHT - top_icon_sz) // 2, top_icon_sz, top_icon_sz).collidepoint(rel_x, rel_y):
            self.go_back()
            return
        nav_x += int(24 * scale)

        # Forward button
        if pygame.Rect(nav_x, (self.TITLEBAR_HEIGHT - top_icon_sz) // 2, top_icon_sz, top_icon_sz).collidepoint(rel_x, rel_y):
            self.go_forward()
            return
        nav_x += int(24 * scale)

        # Up button
        if pygame.Rect(nav_x, (self.TITLEBAR_HEIGHT - top_icon_sz) // 2, top_icon_sz, top_icon_sz).collidepoint(rel_x, rel_y):
            self.go_up()

    def _handle_content_click(self, rel_x, rel_y, scale, ww, wh):
        """Handle clicks inside main application bounds."""
        bottom_margin = int(20 * scale)
        left_w = max(145, int(ww * 0.185))
        center_w = max(48, int(ww * 0.065))

        left_panel_rect = pygame.Rect(16, self.TITLEBAR_HEIGHT + 10, left_w, wh - self.TITLEBAR_HEIGHT - bottom_margin - 10)
        center_strip_rect = pygame.Rect(left_panel_rect.right + 10, self.TITLEBAR_HEIGHT + 10, center_w, wh - self.TITLEBAR_HEIGHT - bottom_margin - 10)

        if left_panel_rect.collidepoint(rel_x, rel_y):
            self._handle_sidebar_click(rel_x, rel_y, left_panel_rect, scale)
            return

        if center_strip_rect.collidepoint(rel_x, rel_y):
            self._handle_center_strip_click(rel_x, rel_y, center_strip_rect, scale)
            return

        if self.current_folder is not None:
            self._handle_folder_item_click(rel_x, rel_y, scale)
            return

        self.selected_item = None

    def _handle_sidebar_click(self, rel_x, rel_y, panel_rect, scale):
        """Handle clicks on sidebar items."""
        y = panel_rect.y + int(10 * scale)
        item_h = max(24, int(panel_rect.height * 0.054))

        for name, path in self.sidebar_items:
            item_rect = pygame.Rect(panel_rect.x + 6, y, panel_rect.width - 12, item_h)
            if item_rect.collidepoint(rel_x, rel_y):
                self.selected_sidebar = name
                if name == "Computer":
                    self.navigate_to(None)
                elif self.filesystem and hasattr(self.filesystem, "get_special_folder"):
                    folder = self.filesystem.get_special_folder(path)
                    if folder:
                        self.navigate_to(folder)
                return
            y += item_h + int(2 * scale)

    def _handle_center_strip_click(self, rel_x, rel_y, strip_rect, scale):
        """Handle clicks on center strip items."""
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
            base_ring_rect = pygame.Rect(strip_rect.centerx - ring_size // 2, y, ring_size, ring_size)
            if base_ring_rect.collidepoint(rel_x, rel_y):
                self.selected_sidebar = key_name
                if self.filesystem and hasattr(self.filesystem, "get_special_folder"):
                    folder = self.filesystem.get_special_folder(path)
                    if folder:
                        self.navigate_to(folder)
                return
            y += spacing_y

    def _on_file_double_click(self, selected_item):
        """Triggered when an item in the file view is double-clicked."""
        if getattr(selected_item, "is_directory", False):
            self.navigate_to(selected_item.path)
            return

        virtual_file = getattr(selected_item, "file_object", selected_item)
        file_name = getattr(virtual_file, "name", "")

        if file_name.endswith((".txt", ".md", ".py", ".json", ".csv", ".log")) or "." not in file_name:
            editor_window = self.desktop.launch_app("Text Editor")
            if editor_window:
                editor_window.open_virtual_file(virtual_file)
                self.desktop.window_manager.focus_window(editor_window)

    def _handle_folder_item_click(self, rel_x, rel_y, scale):
        """Handle single and double clicks on items in the main folder view."""
        clicked_item = None
        for rect, child in self.item_rects:
            if rect.collidepoint(rel_x, rel_y):
                clicked_item = child
                break

        if clicked_item is not None:
            item_name = getattr(clicked_item, "name", "Unknown")
            now = time.time()

            is_double_click = False
            if self.last_clicked is not None:
                last_name = getattr(self.last_clicked, "name", "")
                delta = now - self.last_click_time
                is_double_click = (last_name == item_name and delta < self.double_click_time)

            if is_double_click:
                if self._is_item_folder(clicked_item):
                    self.navigate_to(clicked_item)
                else:
                    self.open_item(clicked_item)
                self.last_clicked = None
                self.last_click_time = 0.0
            else:
                self.selected_item = clicked_item
                self.last_clicked = clicked_item
                self.last_click_time = now
        else:
            self.selected_item = None
            self.last_clicked = None
            self.last_click_time = 0.0

    def _begin_drag(self, mouse_pos):
        """
        Begin a potential drag operation.
        We don't immediately move anything.
        """

        if self.current_folder is None:
            return

        clicked_item = None

        for rect, item in self.item_rects:

            if rect.collidepoint(mouse_pos):
                clicked_item = item
                break

        if clicked_item is None:
            return

        self.selected_item = clicked_item

        self.dragging_item = clicked_item
        self.drag_start_pos = mouse_pos
        self.dragging = False
        self.drop_target = None

    def _update_drag(self, mouse_pos):
        """
        Detect when a normal click becomes a drag and
        determine which folder is currently underneath it.
        """

        if self.dragging_item is None:
            return

        start_x, start_y = self.drag_start_pos
        current_x, current_y = mouse_pos

        distance = (
            (current_x - start_x) ** 2
            + (current_y - start_y) ** 2
        ) ** 0.5

        # Don't start dragging until the mouse has
        # actually moved a little.
        if not self.dragging and distance >= self.drag_threshold:
            self.dragging = True

        if not self.dragging:
            return

        self.drop_target = None

        # Find folder underneath cursor
        for rect, item in self.item_rects:

            if not rect.collidepoint(mouse_pos):
                continue

            # A file cannot be a drop target.
            if not self._is_item_folder(item):
                continue

            # Never allow Computer to be a drop target.
            if self._is_computer_item(item):
                continue

            # Don't drop a folder onto itself.
            if item is self.dragging_item:
                continue

            self.drop_target = item
            break

    def _is_computer_item(self, item):
        """
        Computer is the Explorer dashboard/root view,
        not a real directory that can receive files.
        """

        if item is None:
            return False

        name = getattr(item, "name", "")

        return str(name).strip().lower() == "computer"

    def _finish_drag(self, mouse_pos):
        """
        Complete a drag operation.
        """

        if self.dragging_item is None:
            return

        dragged_item = self.dragging_item
        target_folder = self.drop_target

        was_dragging = self.dragging

        # Reset drag state first
        self.dragging_item = None
        self.dragging = False
        self.drop_target = None

        if not was_dragging:
            return

        if target_folder is None:
            return

        if dragged_item is target_folder:
            return

        self._move_item_to_folder(
            dragged_item,
            target_folder
        )

    def _move_item_to_folder(self, item, destination_folder):
        """
        Move an Explorer item into another directory.
        """

        if self.current_folder is None:
            return False

        if destination_folder is None:
            return False

        if self._is_computer_item(destination_folder):
            print("[VOS] Computer cannot receive dropped items.")
            return False

        item_name = getattr(item, "name", None)

        if not item_name:
            return False

        destination_name = getattr(
            destination_folder,
            "name",
            None
        )

        if not destination_name:
            return False

        # Don't move an item onto itself.
        if item is destination_folder:
            return False

        try:

            # --------------------------------------------------
            # Preferred filesystem API
            # --------------------------------------------------

            if hasattr(self.filesystem, "move_file"):

                source_path = self._get_item_path(
                    item,
                    self.current_folder
                )

                destination_path = self._get_item_path(
                    destination_folder,
                    None
                )

                if source_path and destination_path:

                    final_path = (
                        destination_path.rstrip("/")
                        + "/"
                        + item_name
                    )

                    success = self.filesystem.move_file(
                        source_path,
                        final_path
                    )

                    if success:
                        print(
                            f"[VOS] Moved '{item_name}' "
                            f"to '{destination_name}'"
                        )

                        self._refresh_current_folder()
                        return True

            # --------------------------------------------------
            # Fallback for Folder objects
            # --------------------------------------------------

            source_folder = self.current_folder

            is_folder = self._is_item_folder(item)

            if is_folder:

                if (
                    hasattr(source_folder, "folders")
                    and hasattr(destination_folder, "folders")
                ):

                    if isinstance(source_folder.folders, dict):

                        if item_name in source_folder.folders:

                            moved = source_folder.folders.pop(
                                item_name
                            )

                            destination_folder.folders[
                                item_name
                            ] = moved

                            if hasattr(moved, "parent"):
                                moved.parent = destination_folder

                            self._save_filesystem()
                            self._refresh_current_folder()

                            return True

            else:

                if (
                    hasattr(source_folder, "files")
                    and hasattr(destination_folder, "files")
                ):

                    if isinstance(source_folder.files, dict):

                        if item_name in source_folder.files:

                            content = source_folder.files.pop(
                                item_name
                            )

                            destination_folder.files[
                                item_name
                            ] = content

                            self._save_filesystem()
                            self._refresh_current_folder()

                            return True

            print(
                f"[VOS] Failed to move '{item_name}'"
            )

            return False

        except Exception as e:

            print(
                f"[VOS] Move failed: {e}"
            )

            return False

    def _get_item_path(self, item, parent_folder=None):
        """
        Resolve a VOS item's virtual path.
        """

        path = getattr(item, "path", None)

        if path:
            return str(path)

        name = getattr(item, "name", None)

        if not name:
            return None

        parent = parent_folder

        if parent is None:
            parent = getattr(item, "parent", None)

        parent_path = getattr(parent, "path", None)

        if parent_path:

            parent_path = str(parent_path).rstrip("/")

            if parent_path == "":
                return f"/{name}"

            return f"{parent_path}/{name}"

        return f"/{name}"

    def _save_filesystem(self):
        try:

            if self.filesystem and hasattr(self.filesystem, "save"):
                self.filesystem.save()

            elif hasattr(vos_api, "storage") and hasattr(vos_api.storage, "save"):
                vos_api.storage.save()

        except Exception as e:
            print(f"[VOS] Failed to save filesystem: {e}")

    def _create_ghost_image(self, item):
        item_name = getattr(item, "name", "Unknown")
        is_folder = self._is_item_folder(item)

        ghost = pygame.Surface((100, 40), pygame.SRCALPHA)
        pygame.draw.rect(ghost, (255, 255, 255, 200), (0, 0, 100, 40), border_radius=8)
        pygame.draw.rect(ghost, (200, 200, 200, 100), (0, 0, 100, 40), border_radius=8, width=2)

        icon_size = 24
        icon = self._get_scaled_icon("folder", icon_size) if is_folder else self._get_file_icon(item_name, icon_size)
        if icon:
            ghost.blit(icon, (8, 8))

        font = pygame.font.SysFont("Segoe UI", 11)
        text = font.render(item_name[:15], True, (50, 50, 55))
        ghost.blit(text, (40, 12))

        return ghost
















                