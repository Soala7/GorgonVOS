# editor_input.py
from __future__ import annotations
import pygame
from typing import Any
from desktop.ui.core.event import KeyPressEvent, MousePressEvent, MouseWheelEvent


class EditorInputHandler:
    """Processes user events, routing keystrokes and clicks to buffer and viewport controls."""

    def __init__(self, window: Any) -> None:
        self.window = window

    def handle_event(self, event: Any) -> None:
        if isinstance(event, KeyPressEvent):
            self._handle_keyboard(event)
        elif isinstance(event, MousePressEvent):
            self._handle_mouse(event)
        elif isinstance(event, MouseWheelEvent):
            self._handle_scroll(event)

    def _handle_keyboard(self, event: KeyPressEvent) -> None:
        mods = pygame.key.get_mods()

        if mods & pygame.KMOD_CTRL:
            if self._handle_shortcuts(event):
                return

        key = getattr(event, "key", None)
        buffer = self.window.buffer

        if key == pygame.K_BACKSPACE:
            buffer.delete_backspace()
            self.window.mark_dirty()
        elif key == pygame.K_DELETE:
            buffer.delete_forward()
            self.window.mark_dirty()
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            buffer.insert_newline()
            self.window.mark_dirty()
        elif key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
            self._move_cursor(key)
        elif key == pygame.K_TAB:
            buffer.insert_char("    ")
            self.window.mark_dirty()
        else:
            char = getattr(event, "unicode", None)
            if not char and hasattr(event, "char"):
                char = event.char
            if not char and key is not None and key < 128:
                try:
                    char = chr(key)
                    if mods & pygame.KMOD_SHIFT and char.isalpha():
                        char = char.upper()
                except ValueError:
                    char = None

            if char and char.isprintable() and not (mods & (pygame.KMOD_CTRL | pygame.KMOD_ALT)):
                buffer.insert_char(char)
                self.window.mark_dirty()

        self.window.ensure_cursor_visible()

    def _handle_shortcuts(self, event: KeyPressEvent) -> bool:
        key = getattr(event, "key", None)

        if key == pygame.K_s:
            self.window.save_file()
            return True
        elif key == pygame.K_n:
            self.window.new_file()
            return True
        elif key == pygame.K_f:
            self.window.toggle_search()
            return True

        return False

    def _move_cursor(self, key: int) -> None:
        buffer = self.window.buffer
        layout = self.window.layout

        if key == pygame.K_LEFT:
            if buffer.cursor_col > 0:
                buffer.cursor_col -= 1
            elif buffer.cursor_row > 0:
                buffer.cursor_row -= 1
                buffer.cursor_col = len(buffer.lines[buffer.cursor_row])
            self.window.update_target_x()

        elif key == pygame.K_RIGHT:
            if buffer.cursor_col < len(buffer.lines[buffer.cursor_row]):
                buffer.cursor_col += 1
            elif buffer.cursor_row < len(buffer.lines) - 1:
                buffer.cursor_row += 1
                buffer.cursor_col = 0
            self.window.update_target_x()

        elif key in (pygame.K_UP, pygame.K_DOWN):
            self.window.update_layout()
            v_idx, _ = layout.get_cursor_visual_info(buffer.cursor_row, buffer.cursor_col)
            target_v_idx = v_idx - 1 if key == pygame.K_UP else v_idx + 1

            if 0 <= target_v_idx < len(layout.visual_lines):
                target_vline = layout.visual_lines[target_v_idx]
                buffer.cursor_row = target_vline["row"]
                buffer.cursor_col = (
                    target_vline["col_start"]
                    + layout.get_col_from_x_offset(
                        target_vline["text"], self.window.target_cursor_x
                    )
                )

        self.window.reset_cursor_blink()

    def _handle_mouse(self, event: MousePressEvent) -> None:
        if getattr(event, "button", None) != 1:
            return

        pos = getattr(event, "pos", pygame.mouse.get_pos())
        page_rect = self.window.get_page_rect()

        if page_rect.collidepoint(pos):
            rel_x = max(0, pos[0] - (page_rect.x + self.window.page_padding_x))
            rel_y = pos[1] - (page_rect.y + self.window.page_padding_y)

            target_v_idx = self.window.scroll_y + (rel_y // self.window.line_height)
            target_v_idx = max(0, min(target_v_idx, len(self.window.layout.visual_lines) - 1))

            if self.window.layout.visual_lines:
                target_vline = self.window.layout.visual_lines[target_v_idx]
                self.window.buffer.cursor_row = target_vline["row"]
                self.window.buffer.cursor_col = (
                    target_vline["col_start"]
                    + self.window.layout.get_col_from_x_offset(target_vline["text"], rel_x)
                )

            self.window.update_target_x()
            self.window.reset_cursor_blink()

    def _handle_scroll(self, event: MouseWheelEvent) -> None:
        scroll_val = getattr(event, "y", 0)
        self.window.scroll_y -= scroll_val
        max_scroll = max(0, len(self.window.layout.visual_lines) - 1)
        self.window.scroll_y = max(0, min(self.window.scroll_y, max_scroll))











