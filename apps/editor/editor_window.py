"""
VOS Text Editor Window - LibreOffice Writer Clone
Single-File Implementation with VFS Storage Hooks
"""

from __future__ import annotations

import pygame

from desktop.ui.core.event import (
    KeyPressEvent,
    MousePressEvent,
    MouseWheelEvent,
)
from desktop.ui.window.window import Window


class EditorWindow(Window):

    def __init__(self):
        super().__init__(
            title="Text Editor - LibreOffice Writer",
            width=850,
            height=650,
        )

        self.minimized = False
        self.closed = False

        self.transform.position.x = 200
        self.transform.position.y = 100

        self.is_active = False

        # Fonts
        self.font = pygame.font.SysFont("Calibri", 19, bold=True)
        self.status_font = pygame.font.SysFont("Segoe UI", 14)

        # File & Buffer State
        self.current_file = None  # Holds reference to VirtualFile
        self.file_name = "Untitled.txt"
        self.is_dirty = False
        self.lines = [""]
        self.visual_lines = []

        # Cursor State
        self.cursor_row = 0
        self.cursor_col = 0
        self.cursor_visible = True
        self.cursor_timer = 0.0

        # Viewport & Dimensions
        self.scroll_y = 0
        self.page_padding_x = 20
        self.page_padding_y = 15
        self.line_height = 26
        self.status_bar_height = 24

        self._last_width = -1
        self._needs_layout_update = True

    # --------------------------------------------------
    # VFS File Operations
    # --------------------------------------------------

    def open_virtual_file(self, virtual_file):
        """Loads text content from a VFS VirtualFile object."""
        self.current_file = virtual_file
        self.file_name = getattr(virtual_file, "name", "Untitled.txt")
        
        content = ""
        if hasattr(virtual_file, "read_text"):
            content = virtual_file.read_text()
        elif hasattr(virtual_file, "content"):
            content = str(virtual_file.content)

        self.lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        if not self.lines:
            self.lines = [""]

        self.cursor_row = 0
        self.cursor_col = 0
        self.is_dirty = False
        self._needs_layout_update = True
        self.title = f"{self.file_name} - Text Editor"

    def save_file(self) -> bool:
        """Saves current buffer back to the open VFS VirtualFile."""
        if not self.current_file:
            return False  # Needs Save As dialog

        content = "\n".join(self.lines)
        if hasattr(self.current_file, "write_text"):
            self.current_file.write_text(content)
        elif hasattr(self.current_file, "content"):
            self.current_file.content = content

        self.is_dirty = False
        self.title = f"{self.file_name} - Text Editor"
        return True

    # --------------------------------------------------
    # Event Handling & Dispatching
    # --------------------------------------------------

    def activate(self):
        self._reset_cursor_blink()
        super().activate()
        self.is_active = True

    def deactivate(self):
        self.cursor_visible = False
        self.cursor_timer = 0.0
        super().deactivate()
        self.is_active = False

    def handle_event(self, event):
        super().handle_event(event)

        if not self.is_active or self.minimized:
            return

        # Explicit type checking prevents duplicate key events
        if isinstance(event, KeyPressEvent):
            self._handle_keyboard(event)
        elif isinstance(event, MousePressEvent):
            self._handle_mouse(event)
        elif isinstance(event, MouseWheelEvent):
            self._handle_scroll(event)

    def _handle_keyboard(self, event):
        self._update_layout()
        mods = pygame.key.get_mods()

        # Keyboard Shortcuts (Ctrl + Key)
        if mods & pygame.KMOD_CTRL:
            if self._handle_shortcuts(event):
                return

        key = getattr(event, "key", None)
        if key == pygame.K_BACKSPACE:
            self._delete_backspace()
        elif key == pygame.K_DELETE:
            self._delete_forward()
        elif key == pygame.K_RETURN:
            self._insert_newline()
        elif key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
            self._move_cursor(key)
        elif hasattr(event, "unicode") and event.unicode and event.unicode.isprintable():
            self._insert_character(event.unicode)

        self._update_layout()
        self._ensure_cursor_visible()

    def _handle_shortcuts(self, event) -> bool:
        key = getattr(event, "key", None)

        if key == pygame.K_s:
            self.save_file()
            return True
        elif key == pygame.K_n:
            self.lines = [""]
            self.cursor_row = 0
            self.cursor_col = 0
            self.current_file = None
            self.file_name = "Untitled.txt"
            self.is_dirty = False
            self.title = "Untitled.txt - Text Editor"
            self._needs_layout_update = True
            return True

        return False

    def _handle_mouse(self, event):
        if event.button != 1:
            return

        wx, wy = self.transform.position.x, self.transform.position.y
        ww, wh = self.transform.size.width, self.transform.size.height
        client = pygame.Rect(wx + 2, wy + 38, ww - 4, wh - 40)
        page_rect = self._get_page_rect(client)

        if page_rect.collidepoint(event.pos):
            rel_x = max(0, event.pos[0] - (page_rect.x + self.page_padding_x))
            rel_y = event.pos[1] - (page_rect.y + self.page_padding_y)

            target_v_idx = self.scroll_y + (rel_y // self.line_height)
            target_v_idx = max(0, min(target_v_idx, len(self.visual_lines) - 1))
            target_vline = self.visual_lines[target_v_idx]

            self.cursor_row = target_vline["row"]
            self.cursor_col = target_vline["col_start"] + self._get_col_from_x_offset(
                target_vline["text"], rel_x
            )
            self._reset_cursor_blink()

    def _handle_scroll(self, event):
        self.scroll_y -= event.y
        max_scroll = max(0, len(self.visual_lines) - 1)
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))

    # --------------------------------------------------
    # Text Buffer Actions
    # --------------------------------------------------

    def _insert_character(self, ch: str):
        line = self.lines[self.cursor_row]
        self.lines[self.cursor_row] = line[:self.cursor_col] + ch + line[self.cursor_col:]
        self.cursor_col += len(ch)
        self._mark_dirty()

    def _insert_newline(self):
        line = self.lines[self.cursor_row]
        left, right = line[:self.cursor_col], line[self.cursor_col:]
        self.lines[self.cursor_row] = left
        self.lines.insert(self.cursor_row + 1, right)
        self.cursor_row += 1
        self.cursor_col = 0
        self._mark_dirty()

    def _delete_backspace(self):
        if self.cursor_col > 0:
            line = self.lines[self.cursor_row]
            self.lines[self.cursor_row] = line[:self.cursor_col - 1] + line[self.cursor_col:]
            self.cursor_col -= 1
            self._mark_dirty()
        elif self.cursor_row > 0:
            previous = self.lines[self.cursor_row - 1]
            current = self.lines.pop(self.cursor_row)
            self.cursor_row -= 1
            self.cursor_col = len(previous)
            self.lines[self.cursor_row] = previous + current
            self._mark_dirty()

    def _delete_forward(self):
        line = self.lines[self.cursor_row]
        if self.cursor_col < len(line):
            self.lines[self.cursor_row] = line[:self.cursor_col] + line[self.cursor_col + 1:]
            self._mark_dirty()
        elif self.cursor_row < len(self.lines) - 1:
            self.lines[self.cursor_row] += self.lines.pop(self.cursor_row + 1)
            self._mark_dirty()

    def _move_cursor(self, key):
        if key == pygame.K_LEFT:
            if self.cursor_col > 0:
                self.cursor_col -= 1
            elif self.cursor_row > 0:
                self.cursor_row -= 1
                self.cursor_col = len(self.lines[self.cursor_row])
        elif key == pygame.K_RIGHT:
            if self.cursor_col < len(self.lines[self.cursor_row]):
                self.cursor_col += 1
            elif self.cursor_row < len(self.lines) - 1:
                self.cursor_row += 1
                self.cursor_col = 0
        elif key in (pygame.K_UP, pygame.K_DOWN):
            v_idx, x_off = self._get_cursor_visual_info()
            target_v_idx = v_idx - 1 if key == pygame.K_UP else v_idx + 1
            if 0 <= target_v_idx < len(self.visual_lines):
                target_vline = self.visual_lines[target_v_idx]
                self.cursor_row = target_vline["row"]
                self.cursor_col = target_vline["col_start"] + self._get_col_from_x_offset(
                    target_vline["text"], x_off
                )
        self._reset_cursor_blink()

    def _mark_dirty(self):
        self.is_dirty = True
        self._needs_layout_update = True
        self.title = f"{self.file_name}* - Text Editor"
        self._reset_cursor_blink()

    # --------------------------------------------------
    # Layout & Cursor Helpers
    # --------------------------------------------------

    def _reset_cursor_blink(self):
        self.cursor_visible = True
        self.cursor_timer = 0.0

    def _get_page_rect(self, client: pygame.Rect) -> pygame.Rect:
        page_width = min(810, client.width - 20)
        page_width = max(300, page_width)
        page_height = client.height - self.status_bar_height - 10
        page_x = client.x + (client.width - page_width) // 2
        page_y = client.y + 5
        return pygame.Rect(page_x, page_y, page_width, page_height)

    def _update_layout(self):
        ww = self.transform.size.width
        if not self._needs_layout_update and ww == self._last_width:
            return

        self._last_width = ww
        self._needs_layout_update = False

        client_w = ww - 4
        page_w = min(810, client_w - 20)
        max_text_width = max(100, page_w - (self.page_padding_x * 2))

        self.visual_lines = []
        for row_idx, line in enumerate(self.lines):
            if not line:
                self.visual_lines.append({"row": row_idx, "col_start": 0, "text": ""})
                continue

            words, word = [], ""
            for char in line:
                word += char
                if char in (" ", "-"):
                    words.append(word)
                    word = ""
            if word:
                words.append(word)

            current_line, start_idx = "", 0
            for w in words:
                test_line = current_line + w
                if self.font.size(test_line)[0] > max_text_width and current_line:
                    self.visual_lines.append(
                        {"row": row_idx, "col_start": start_idx, "text": current_line}
                    )
                    start_idx += len(current_line)
                    current_line = w
                else:
                    current_line = test_line

            if current_line:
                self.visual_lines.append(
                    {"row": row_idx, "col_start": start_idx, "text": current_line}
                )

        self.scroll_y = min(self.scroll_y, max(0, len(self.visual_lines) - 1))

    def _get_cursor_visual_info(self):
        if not self.visual_lines:
            return 0, 0

        for i, vline in enumerate(self.visual_lines):
            if vline["row"] != self.cursor_row:
                continue

            end_col = vline["col_start"] + len(vline["text"])
            is_last_chunk = True
            if i + 1 < len(self.visual_lines) and self.visual_lines[i + 1]["row"] == self.cursor_row:
                is_last_chunk = False

            if vline["col_start"] <= self.cursor_col < end_col:
                rel_col = self.cursor_col - vline["col_start"]
                return i, self.font.size(vline["text"][:rel_col])[0]
            elif is_last_chunk and self.cursor_col >= end_col:
                return i, self.font.size(vline["text"])[0]

        return 0, 0

    def _get_col_from_x_offset(self, text, target_x):
        best_col, min_dist = 0, float("inf")
        for col in range(len(text) + 1):
            dist = abs(self.font.size(text[:col])[0] - target_x)
            if dist < min_dist:
                min_dist, best_col = dist, col
        return best_col

    def _ensure_cursor_visible(self):
        v_idx, _ = self._get_cursor_visual_info()
        client_height = self.transform.size.height - 64
        visible_lines_count = max(1, (client_height - (self.page_padding_y * 2)) // self.line_height)

        if v_idx < self.scroll_y:
            self.scroll_y = v_idx
        elif v_idx >= self.scroll_y + visible_lines_count:
            self.scroll_y = v_idx - visible_lines_count + 1

    # --------------------------------------------------
    # Rendering Pipeline
    # --------------------------------------------------

    def update(self, dt):
        super().update(dt)
        if self.is_active:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_timer = 0.0
                self.cursor_visible = not self.cursor_visible
            self._update_layout()
            self._ensure_cursor_visible()

    def draw(self, renderer):
        if self.minimized:
            return

        super().draw(renderer)
        surface = renderer.surface

        wx, wy = self.transform.position.x, self.transform.position.y
        ww, wh = self.transform.size.width, self.transform.size.height
        client = pygame.Rect(wx + 2, wy + 38, ww - 4, wh - 40)

        old_clip = surface.get_clip()
        surface.set_clip(client)

        page_rect = self._get_page_rect(client)

        self._draw_workspace(surface, client, page_rect)
        self._draw_document_content(surface, page_rect)
        self._draw_statusbar(surface, client)

        surface.set_clip(old_clip)

    def _draw_workspace(self, surface, client, page_rect):
        pygame.draw.rect(surface, (215, 218, 224), client)
        shadow_rect = pygame.Rect(page_rect.x + 3, page_rect.y + 3, page_rect.width, page_rect.height)
        pygame.draw.rect(surface, (170, 175, 185), shadow_rect)
        pygame.draw.rect(surface, (255, 255, 255), page_rect)
        pygame.draw.rect(surface, (190, 195, 205), page_rect, 1)

    def _draw_document_content(self, surface, page_rect):
        self._update_layout()
        visible_lines_count = max(1, (page_rect.height - (self.page_padding_y * 2)) // self.line_height)
        start_index = max(0, self.scroll_y)
        end_index = min(len(self.visual_lines), start_index + visible_lines_count + 1)

        base_x = page_rect.x + self.page_padding_x
        base_y = page_rect.y + self.page_padding_y
        cursor_v_idx, cursor_x_off = self._get_cursor_visual_info()

        for idx in range(start_index, end_index):
            vline = self.visual_lines[idx]
            render_y = base_y + (idx - self.scroll_y) * self.line_height

            # 2px Black Ruled Document Line
            guide_y = render_y + self.line_height - 2
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (base_x - 5, guide_y),
                (page_rect.x + page_rect.width - self.page_padding_x + 5, guide_y),
                2,
            )

            # Active Line Highlight
            if idx == cursor_v_idx and self.is_active:
                h_rect = pygame.Rect(
                    base_x - 5, render_y, page_rect.width - (self.page_padding_x * 2) + 10, self.line_height
                )
                pygame.draw.rect(surface, (235, 243, 250), h_rect)

            # Text Rendering
            img = self.font.render(vline["text"], True, (0, 0, 0))
            surface.blit(img, (base_x, render_y))

        # Cursor Rendering
        if self.cursor_visible and self.is_active and (start_index <= cursor_v_idx < end_index):
            cursor_y = base_y + (cursor_v_idx - self.scroll_y) * self.line_height
            pygame.draw.rect(surface, (0, 0, 0), (base_x + cursor_x_off, cursor_y + 2, 2, self.line_height - 4))

    def _draw_statusbar(self, surface, client):
        status_rect = pygame.Rect(
            client.x, client.y + client.height - self.status_bar_height, client.width, self.status_bar_height
        )
        pygame.draw.rect(surface, (235, 238, 242), status_rect)
        pygame.draw.line(surface, (200, 205, 215), (status_rect.x, status_rect.y), (status_rect.x + status_rect.width, status_rect.y))

        word_count = sum(len(l.split()) for l in self.lines)
        dirty_flag = "*" if self.is_dirty else ""
        status_text = f" {self.file_name}{dirty_flag} | Line {self.cursor_row + 1}, Col {self.cursor_col + 1} | Words: {word_count} | 100%"
        status_surf = self.status_font.render(status_text, True, (80, 85, 95))
        surface.blit(status_surf, (status_rect.x + 10, status_rect.y + 3))


    def save_file(self) -> bool:
        """Writes the current line buffer back to VirtualFS and flushes to disk."""
        if not self.current_file:
            # File has not been saved before - prompt Save As (or return False)
            return False

        # 1. Update in-memory VirtualFile node content
        content = "\n".join(self.lines)
        if hasattr(self.current_file, "write_text"):
            self.current_file.write_text(content)
        elif hasattr(self.current_file, "content"):
            self.current_file.content = content

        # 2. Persist VFS state to storage disk file (data/VOS.os)
        if hasattr(self, "desktop") and self.desktop:
            if hasattr(self.desktop, "storage"):
                self.desktop.storage.save()
            elif hasattr(self.desktop, "filesystem") and hasattr(self.desktop.filesystem, "save"):
                self.desktop.filesystem.save()

        # 3. Reset dirty state and refresh window title
        self.is_dirty = False
        self.title = f"{self.file_name} - Text Editor"
        return True






















