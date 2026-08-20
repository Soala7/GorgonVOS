

from __future__ import annotations

import pygame

from desktop.ui.core.event import KeyPressEvent
from desktop.ui.window.window import Window
from resources.cursor_manager import cursor_manager
from desktop.assests.icon_manager import IconManager
from bridge.vos_api import vos_api

from .editor_buffer import EditorBuffer
from .editor_layout import EditorLayout
from .editor_render import EditorRender
from .editor_input import EditorInputHandler
from .editor_menu import EditorMenu
from .editor_search import EditorSearch
from .editor_toolbar import EditorToolbar
from .editor_tabs import EditorTabManager

class SaveAsDialog:
    """Modal dialog for choosing a target directory and file name."""

    def __init__(
        self,
        default_dir: str,
        default_name: str,
        on_submit,
    ):
        self.directory = default_dir
        self.filename = default_name
        self.on_submit = on_submit
        self.is_active = True

        self.font = pygame.font.SysFont("Segoe UI", 14)

    def handle_event(self, event) -> bool:
        if not self.is_active:
            return False

        evt_type = getattr(
            event,
            "type",
            getattr(event, "event_type", None),
        )

        if callable(evt_type):
            evt_type = evt_type()

        type_str = str(type(event)).upper()
        evt_str = str(evt_type).upper()

        if "RELEASE" in type_str or "UP" in evt_str:
            return True

        is_keydown = (
            evt_type == pygame.KEYDOWN
            or "KEYDOWN" in evt_str
            or "KEY" in type_str
        )

        if is_keydown:
            key = getattr(event, "key", None)

            if callable(key):
                key = key()

            unicode_char = getattr(
                event,
                "unicode",
                getattr(
                    event,
                    "char",
                    getattr(event, "text", ""),
                ),
            )

            if callable(unicode_char):
                unicode_char = unicode_char()

            if key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                13,
                1073741912,
            ):
                clean_dir = self.directory.rstrip("/")
                clean_file = self.filename.strip()

                full_path = (
                    f"{clean_dir}/{clean_file}"
                    if clean_dir
                    else f"/{clean_file}"
                )

                self.is_active = False
                self.on_submit(full_path)

                return True

            elif key in (pygame.K_ESCAPE, 27):
                self.is_active = False
                return True

            elif key in (pygame.K_BACKSPACE, 8):
                self.filename = self.filename[:-1]
                return True

            else:
                if unicode_char and str(unicode_char).isprintable():
                    self.filename += str(unicode_char)
                    return True

                elif isinstance(key, int) and 32 <= key <= 126:
                    self.filename += chr(key)
                    return True

        return True

    def draw(
        self,
        surface: pygame.Surface,
        client_rect: pygame.Rect,
    ) -> None:
        if not self.is_active:
            return

        overlay = pygame.Surface(
            (client_rect.width, client_rect.height),
            pygame.SRCALPHA,
        )

        overlay.fill((0, 0, 0, 120))
        surface.blit(
            overlay,
            (client_rect.x, client_rect.y),
        )

        box_w, box_h = 420, 160

        dialog_rect = pygame.Rect(
            client_rect.centerx - (box_w // 2),
            client_rect.centery - (box_h // 2),
            box_w,
            box_h,
        )

        pygame.draw.rect(
            surface,
            (38, 38, 42),
            dialog_rect,
        )

        pygame.draw.rect(
            surface,
            (0, 122, 204),
            dialog_rect,
            2,
        )

        lbl_title = self.font.render(
            "Save File As",
            True,
            (255, 255, 255),
        )

        lbl_dir = self.font.render(
            f"Directory: {self.directory}",
            True,
            (170, 170, 170),
        )

        surface.blit(
            lbl_title,
            (dialog_rect.x + 15, dialog_rect.y + 12),
        )

        surface.blit(
            lbl_dir,
            (dialog_rect.x + 15, dialog_rect.y + 35),
        )

        input_box = pygame.Rect(
            dialog_rect.x + 15,
            dialog_rect.y + 65,
            390,
            30,
        )

        pygame.draw.rect(
            surface,
            (20, 20, 22),
            input_box,
        )

        pygame.draw.rect(
            surface,
            (0, 122, 204),
            input_box,
            1,
        )

        txt_name = self.font.render(
            self.filename,
            True,
            (255, 255, 255),
        )

        surface.blit(
            txt_name,
            (input_box.x + 8, input_box.y + 5),
        )

        lbl_hint = self.font.render(
            "[ENTER] Confirm | [ESC] Cancel",
            True,
            (120, 120, 120),
        )

        surface.blit(
            lbl_hint,
            (dialog_rect.x + 15, dialog_rect.y + 115),
        )

class EditorWindow(Window):
    """Main modularized Text Editor window coordinating core subsystems."""

    TITLEBAR_HEIGHT = 40

    def __init__(
        self,
        title: str = "Text Editor - LibreOffice Writer",
        width: int = 850,
        height: int = 650,
        name: str = "Text Editor",
    ) -> None:

        super().__init__(
            title=title,
            width=width,
            height=height,
            name=name,
        )

        self._init_filesystem()

        self.minimized: bool = False
        self.closed: bool = False
        self.is_active: bool = True

        self.transform.position.x = 200
        self.transform.position.y = 100

        self.font = pygame.font.SysFont(
            "Calibri",
            19,
            bold=True,
        )

        self.status_font = pygame.font.SysFont(
            "Segoe UI",
            14,
        )

        self.tabs = EditorTabManager(height=28)
        self.layout = EditorLayout(self.font)
        self.render = EditorRender(
            self.font,
            self.status_font,
        )
        self.input_handler = EditorInputHandler(self)
        self.file_menu = EditorMenu(self)
        self.search = EditorSearch()
        self.toolbar = EditorToolbar(
            0,
            0,
            width,
        )

        self.dialog: SaveAsDialog | None = None

        self.page_padding_x = 20
        self.page_padding_y = 15
        self.line_height = 26
        self.status_bar_height = 24

        self.cursor_visible = True
        self.cursor_timer = 0.0

        pygame.key.set_repeat(300, 35)

        self._load_icons()
        self.content_cursor = cursor_manager.TEXT

    @property
    def buffer(self) -> EditorBuffer:
        return self.tabs.active_tab.buffer

    @property
    def scroll_y(self) -> int:
        return self.tabs.active_tab.scroll_y

    @scroll_y.setter
    def scroll_y(self, val: int) -> None:
        self.tabs.active_tab.scroll_y = val

    @property
    def target_cursor_x(self) -> float:
        return self.tabs.active_tab.target_cursor_x

    @target_cursor_x.setter
    def target_cursor_x(self, val: float) -> None:
        self.tabs.active_tab.target_cursor_x = val

    def _init_filesystem(self) -> None:
        self.filesystem = None

        if (
            hasattr(vos_api, "filesystem")
            and vos_api.filesystem is not None
        ):
            self.filesystem = vos_api.filesystem

        else:
            try:
                from filesystem.filesystem import FileSystem

                self.filesystem = FileSystem()
                vos_api.filesystem = self.filesystem

            except Exception as exc:
                print(
                    f"[EDITOR][FILESYSTEM] "
                    f"Failed to initialize filesystem: {exc}"
                )

                self.filesystem = None

    def _load_icons(self) -> None:
        size = 24

        self.raw_icons = {
            "save": IconManager.get(
                "editor/save",
                size,
            ),
            "new": IconManager.get(
                "editor/new",
                size,
            ),
            "document": IconManager.get(
                "files/text",
                size,
            ),
        }

    def open_virtual_file(self, virtual_file) -> None:
        file_name = getattr(
            virtual_file,
            "name",
            "Untitled.txt",
        )

        content = ""

        if hasattr(virtual_file, "read_text"):
            content = virtual_file.read_text()

        elif hasattr(virtual_file, "read"):
            content = virtual_file.read()

        elif hasattr(virtual_file, "content"):
            content = str(virtual_file.content)

        print("\n[EDITOR][OPEN]")
        print(f"  file name : {file_name}")
        print(f"  object    : {virtual_file}")
        print(f"  type      : {type(virtual_file)}")
        print(f"  content   : {len(content)} chars")

        active = self.tabs.active_tab

        active.virtual_file = virtual_file
        active.file_name = file_name

        active.buffer.set_text(content)
        active.buffer.is_dirty = False

        self.update_target_x()

        self.title = f"{file_name} - Text Editor"

        print("[EDITOR][OPEN] File loaded into buffer.\n")

    def new_document(self) -> None:
        self.new_file()

    def open_document_dialog(self) -> None:
        print("[EDITOR] Open dialog coming next")

    def save_as_document(self) -> None:
        self.open_save_dialog()

    def save_file(self) -> bool:
        active = self.tabs.active_tab

        print("\n========== [EDITOR SAVE] ==========")

        print(
            f"[EDITOR SAVE] active tab      : {active}"
        )

        print(
            f"[EDITOR SAVE] file name      : "
            f"{getattr(active, 'file_name', None)}"
        )

        print(
            f"[EDITOR SAVE] virtual file  : "
            f"{getattr(active, 'virtual_file', None)}"
        )

        print(
            f"[EDITOR SAVE] virtual type   : "
            f"{type(getattr(active, 'virtual_file', None))}"
        )

        print(
            f"[EDITOR SAVE] buffer type    : "
            f"{type(active.buffer)}"
        )

        print(
            f"[EDITOR SAVE] buffer dirty   : "
            f"{active.buffer.is_dirty}"
        )

        if (
            not active.virtual_file
            or active.file_name == "Untitled.txt"
        ):
            print(
                "[EDITOR SAVE] No existing VirtualFile."
            )
            print(
                "[EDITOR SAVE] Opening Save As dialog."
            )
            print("==================================\n")

            self.open_save_dialog()
            return True

        content = self.buffer.get_text()

        print(
            f"[EDITOR SAVE] content length: "
            f"{len(content)}"
        )

        print(
            f"[EDITOR SAVE] content preview: "
            f"{repr(content[:100])}"
        )

        file_path = getattr(
            active.virtual_file,
            "path",
            None,
        )

        if not file_path:
            print(
                "[EDITOR SAVE] VirtualFile has no path."
            )

            file_path = getattr(
                active.virtual_file,
                "name",
                active.file_name,
            )

        print(
            f"[EDITOR SAVE] target path: {file_path}"
        )

        result = self._write_to_filesystem(
            file_path,
            content,
            existing_file=active.virtual_file,
        )

        print(
            f"[EDITOR SAVE] RESULT: {result}"
        )

        print("==================================\n")

        return result

    def save_to_directory(
        self,
        file_name: str,
        target_dir: str = "/users/guest/Documents",
    ) -> bool:

        full_path = (
            f"{target_dir.rstrip('/')}/{file_name}"
        )

        content = self.buffer.get_text()

        return self._write_to_filesystem(
            full_path,
            content,
        )

    def open_save_dialog(
        self,
        target_dir: str = "/users/guest/Documents",
    ) -> None:

        active = self.tabs.active_tab

        initial_name = (
            active.file_name
            if active.file_name != "Untitled.txt"
            else "document.txt"
        )

        self.dialog = SaveAsDialog(
            default_dir=target_dir,
            default_name=initial_name,
            on_submit=self._on_save_dialog_confirmed,
        )

    def _on_save_dialog_confirmed(
        self,
        target_path: str,
    ) -> None:

        print(
            f"[EDITOR][SAVE AS] Requested: "
            f"{target_path}"
        )

        content = self.buffer.get_text()

        self._write_to_filesystem(
            target_path,
            content,
        )

    def _write_to_filesystem(
        self,
        target_path: str,
        content: str,
        existing_file=None,
    ) -> bool:

        print("\n---------- [FILESYSTEM WRITE] ----------")

        if not self.filesystem:
            print(
                "[EDITOR][WRITE] ERROR: "
                "filesystem is None"
            )
            print("----------------------------------------\n")
            return False

        print(
            f"[EDITOR][WRITE] path    : {target_path}"
        )

        print(
            f"[EDITOR][WRITE] content : "
            f"{len(content)} chars"
        )

        print(
            f"[EDITOR][WRITE] existing: "
            f"{existing_file}"
        )

        print(
            f"[EDITOR][WRITE] existing type: "
            f"{type(existing_file)}"
        )

        if existing_file is not None:

            print(
                "[EDITOR][WRITE] "
                "Updating existing VirtualFile..."
            )

            if hasattr(existing_file, "write_text"):

                existing_file.write_text(content)

                print(
                    "[EDITOR][WRITE] "
                    "VirtualFile.write_text() called."
                )

            elif hasattr(existing_file, "content"):

                existing_file.content = content

                print(
                    "[EDITOR][WRITE] "
                    "VirtualFile.content updated."
                )

            else:

                print(
                    "[EDITOR][WRITE] ERROR: "
                    "Existing object cannot receive text."
                )

                print("----------------------------------------\n")

                return False

            if hasattr(self.filesystem, "save"):

                print(
                    "[EDITOR][WRITE] "
                    "Calling filesystem.save()..."
                )

                self.filesystem.save()

            active = self.tabs.active_tab

            active.buffer.is_dirty = False

            self.title = (
                f"{active.file_name} - Text Editor"
            )

            print(
                "[EDITOR][WRITE] "
                "EXISTING FILE SAVED."
            )

            print("----------------------------------------\n")

            return True

        print(
            "[EDITOR][WRITE] "
            "No existing VirtualFile."
        )

        print(
            "[EDITOR][WRITE] "
            "Creating new file..."
        )

        created = False

        if hasattr(
            self.filesystem,
            "create_file",
        ):

            try:
                created = self.filesystem.create_file(
                    target_path,
                    content,
                )

                print(
                    f"[EDITOR][WRITE] "
                    f"create_file result: {created}"
                )

            except Exception as exc:

                print(
                    "[EDITOR][WRITE] "
                    f"create_file ERROR: {exc}"
                )

        elif (
            hasattr(self.filesystem, "disk")
            and hasattr(
                self.filesystem.disk,
                "create_file",
            )
        ):

            try:

                self.filesystem.disk.create_file(
                    target_path,
                    content,
                )

                created = True

            except Exception as exc:

                print(
                    "[EDITOR][WRITE] "
                    f"disk.create_file ERROR: {exc}"
                )

        if not created:

            print(
                "[EDITOR][WRITE] "
                "Could not create file."
            )

            print("----------------------------------------\n")

            return False

        active = self.tabs.active_tab

        active.file_name = target_path.split("/")[-1]

        new_virtual_file = None

        if hasattr(
            self.filesystem,
            "get_file",
        ):

            try:
                new_virtual_file = (
                    self.filesystem.get_file(
                        target_path
                    )
                )
            except Exception:
                pass

        if new_virtual_file is not None:

            active.virtual_file = new_virtual_file

            print(
                "[EDITOR][WRITE] "
                "Attached new VirtualFile to tab."
            )

        else:

            print(
                "[EDITOR][WRITE] WARNING: "
                "Could not retrieve new VirtualFile."
            )

        active.buffer.is_dirty = False

        self.title = (
            f"{active.file_name} - Text Editor"
        )

        if hasattr(
            self.filesystem,
            "save",
        ):

            print(
                "[EDITOR][WRITE] "
                "Calling filesystem.save()..."
            )

            self.filesystem.save()

        print(
            "[EDITOR][WRITE] "
            "NEW FILE SAVED."
        )

        print("----------------------------------------\n")

        return True

    def new_file(self) -> None:
        self.tabs.new_tab()
        self.title = "Untitled.txt - Text Editor"

    def toggle_search(self) -> None:
        if hasattr(self.search, "visible"):
            self.search.visible = not self.search.visible

    def mark_dirty(self) -> None:
        self.tabs.active_tab.buffer.is_dirty = True

        self.title = (
            f"{self.tabs.active_tab.file_name}* "
            f"- Text Editor"
        )

        self.reset_cursor_blink()

    def reset_cursor_blink(self) -> None:
        self.cursor_visible = True
        self.cursor_timer = 0.0

    def update_layout(self) -> None:
        self.layout.update_layout(
            self.buffer.lines,
            self.transform.size.width,
        )

    def update_target_x(self) -> None:
        self.update_layout()

        _, x_off = (
            self.layout.get_cursor_visual_info(
                self.buffer.cursor_row,
                self.buffer.cursor_col,
            )
        )

        self.target_cursor_x = x_off

    def ensure_cursor_visible(self) -> None:
        v_idx, _ = (
            self.layout.get_cursor_visual_info(
                self.buffer.cursor_row,
                self.buffer.cursor_col,
            )
        )

        client_h = (
            self.transform.size.height
            - (
                self.TITLEBAR_HEIGHT
                + self.status_bar_height
            )
        )

        visible_count = max(
            1,
            (
                client_h
                - (self.page_padding_y * 2)
            )
            // self.line_height,
        )

        if v_idx < self.scroll_y:
            self.scroll_y = v_idx

        elif v_idx >= self.scroll_y + visible_count:
            self.scroll_y = (
                v_idx
                - visible_count
                + 1
            )

    def get_page_rect(self) -> pygame.Rect:

        wx, wy = (
            self.transform.position.x,
            self.transform.position.y,
        )

        ww, wh = (
            self.transform.size.width,
            self.transform.size.height,
        )

        offset_top = (
            self.TITLEBAR_HEIGHT
            + 34
            + 32
        )

        client = pygame.Rect(
            wx + 2,
            wy + offset_top,
            ww - 4,
            wh - (offset_top + 2),
        )

        page_w = min(
            810,
            client.width - 20,
        )

        page_w = max(300, page_w)

        page_h = max(
            100,
            client.height
            - self.status_bar_height
            - 10,
        )

        return pygame.Rect(
            client.x
            + (
                client.width
                - page_w
            )
            // 2,
            client.y + 5,
            page_w,
            page_h,
        )

    def handle_event(self, event) -> None:

        super().handle_event(event)

        if getattr(event, "handled", False):
            return

        evt_type = getattr(
            event,
            "type",
            getattr(event, "event_type", None),
        )

        if evt_type == pygame.MOUSEBUTTONDOWN:
            pos = getattr(event, "pos", pygame.mouse.get_pos())

            wx, wy = (
                self.transform.position.x,
                self.transform.position.y,
            )

            ww, wh = (
                self.transform.size.width,
                self.transform.size.height,
            )

            window_rect = pygame.Rect(wx, wy, ww, wh)

            if window_rect.collidepoint(pos):
                self.is_active = True
                pygame.key.set_repeat(300, 35)
                self.reset_cursor_blink()

        if not self.is_active or self.minimized:
            return

        if isinstance(event, KeyPressEvent) and getattr(self.search, "visible", False):
            if event.key == pygame.K_ESCAPE:
                self.search.visible = False
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                match = self.search.next_match()
                if match:
                    self.buffer.cursor_row, self.buffer.cursor_col = match
                    self.ensure_cursor_visible()
            elif event.key == pygame.K_BACKSPACE:
                self.search.query = self.search.query[:-1]
                self.search.find_in_buffer(self.buffer.lines, self.search.query)
            elif event.unicode and event.unicode.isprintable():
                self.search.query += event.unicode
                self.search.find_in_buffer(self.buffer.lines, self.search.query)
            event.handled = True
            return

        if self.dialog and getattr(self.dialog, "is_active", False):
            if self.dialog.handle_event(event):
                return

        print(
            "[EDITOR EVENT]",
            "type=", getattr(event, "type", None),
            "key=", getattr(event, "key", None),
            "unicode=", repr(getattr(event, "unicode", None)),
        )

        self.input_handler.handle_event(event)

    def update(self, dt: float) -> None:

        if dt is None:
            dt = 0.016

        super().update(dt)

        if self.is_active:

            self.cursor_timer += dt

            if self.cursor_timer >= 0.5:

                self.cursor_timer = 0.0

                self.cursor_visible = (
                    not self.cursor_visible
                )

            self.update_layout()

    def draw(self, renderer) -> None:

        if self.minimized:
            return

        super().draw(renderer)

        surface = renderer.surface

        wx, wy = (
            self.transform.position.x,
            self.transform.position.y,
        )

        ww, wh = (
            self.transform.size.width,
            self.transform.size.height,
        )

        client = pygame.Rect(
            wx + 2,
            wy + self.TITLEBAR_HEIGHT,
            ww - 4,
            wh - (
                self.TITLEBAR_HEIGHT + 2
            ),
        )

        old_clip = surface.get_clip()

        surface.set_clip(client)

        page_rect = self.get_page_rect()

        self.render.draw_workspace(
            surface,
            client,
            page_rect,
        )

        if hasattr(self.toolbar, "rect"):

            self.toolbar.rect.x = client.x
            self.toolbar.rect.y = client.y + 32
            self.toolbar.rect.width = client.width

        if hasattr(self.toolbar, "draw"):

            try:
                self.toolbar.draw(surface)

            except TypeError:
                self.toolbar.draw(
                    surface,
                    client.x,
                    client.y + 32,
                )

        v_idx, x_off = (
            self.layout.get_cursor_visual_info(
                self.buffer.cursor_row,
                self.buffer.cursor_col,
            )
        )

        self.render.draw_content(
            surface,
            page_rect,
            self.layout.visual_lines,
            self.scroll_y,
            v_idx,
            x_off,
            self.cursor_visible,
            self.is_active,
            self.line_height,
            self.page_padding_x,
            self.page_padding_y,
        )

        word_count = sum(
            len(line.split())
            for line in self.buffer.lines
        )

        self.render.draw_statusbar(
            surface,
            client,
            self.tabs.active_tab.file_name,
            self.buffer.is_dirty,
            self.buffer.cursor_row,
            self.buffer.cursor_col,
            word_count,
            self.status_bar_height,
        )

        if getattr(self.search, "visible", False):
            search_rect = pygame.Rect(client.right - 320, client.y + 8, 300, 30)
            pygame.draw.rect(surface, (255, 255, 255), search_rect, border_radius=6)
            pygame.draw.rect(surface, (70, 120, 220), search_rect, 1, border_radius=6)
            query = self.search.query or "Find..."
            color = (35, 40, 50) if self.search.query else (135, 140, 150)
            surface.blit(self.status_font.render(query, True, color), (search_rect.x + 8, search_rect.y + 7))
            if self.search.matches:
                count = f"{self.search.current_match_idx + 1}/{len(self.search.matches)}"
                surface.blit(self.status_font.render(count, True, (80, 90, 110)), (search_rect.right - 45, search_rect.y + 7))

        self.file_menu.draw(surface)

        if (
            self.dialog
            and getattr(
                self.dialog,
                "is_active",
                False,
            )
        ):
            self.dialog.draw(
                surface,
                client,
            )

        surface.set_clip(old_clip)
