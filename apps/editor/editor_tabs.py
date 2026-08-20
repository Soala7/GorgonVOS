
from __future__ import annotations
import pygame
from typing import List, Optional
from .editor_buffer import EditorBuffer

class TabInstance:
    """Encapsulates buffer state and file metadata for an individual tab."""

    def __init__(self, file_name: str = "Untitled.txt", virtual_file=None) -> None:
        self.file_name: str = file_name
        self.virtual_file = virtual_file
        self.buffer: EditorBuffer = EditorBuffer()
        self.scroll_y: int = 0
        self.target_cursor_x: float = 0.0

class EditorTabManager:
    """Handles tab lifecycle, active buffer switching, and tab bar layout."""

    def __init__(self, height: int = 28) -> None:
        self.height = height
        self.tabs: List[TabInstance] = [TabInstance()]
        self.active_idx: int = 0
        self.font = pygame.font.SysFont("Segoe UI", 12)

    @property
    def active_tab(self) -> TabInstance:
        return self.tabs[self.active_idx]

    def new_tab(self, file_name: str = "Untitled.txt", virtual_file=None) -> TabInstance:
        tab = TabInstance(file_name=file_name, virtual_file=virtual_file)
        self.tabs.append(tab)
        self.active_idx = len(self.tabs) - 1
        return tab

    def close_tab(self, idx: int) -> None:
        if len(self.tabs) > 1 and 0 <= idx < len(self.tabs):
            self.tabs.pop(idx)
            self.active_idx = max(0, min(self.active_idx, len(self.tabs) - 1))

    def switch_tab(self, idx: int) -> None:
        if 0 <= idx < len(self.tabs):
            self.active_idx = idx

    def draw(self, surface: pygame.Surface, x: int, y: int, width: int) -> None:
        bar_rect = pygame.Rect(x, y, width, self.height)
        pygame.draw.rect(surface, (220, 223, 228), bar_rect)
        pygame.draw.line(
            surface, (190, 195, 205), (x, y + self.height - 1), (x + width, y + self.height - 1)
        )

        tab_x = x + 5
        for idx, tab in enumerate(self.tabs):
            dirty_flag = "*" if tab.buffer.is_dirty else ""
            title = f"{tab.file_name}{dirty_flag}"
            text_surf = self.font.render(title, True, (30, 30, 30))
            tab_w = max(110, text_surf.get_width() + 25)

            tab_rect = pygame.Rect(tab_x, y + 3, tab_w, self.height - 3)
            is_active = idx == self.active_idx

            bg_color = (255, 255, 255) if is_active else (205, 210, 218)
            pygame.draw.rect(surface, bg_color, tab_rect, border_top_left_radius=4, border_top_right_radius=4)
            pygame.draw.rect(surface, (170, 175, 185), tab_rect, width=1, border_top_left_radius=4, border_top_right_radius=4)

            surface.blit(text_surf, (tab_x + 8, y + 7))
            tab_x += tab_w + 3
