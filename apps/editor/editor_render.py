# editor_render.py
from __future__ import annotations
import pygame
from typing import List, Dict, Any


class EditorRender:
    """Manages workspace, paper background, text surface, and status bar rendering."""

    def __init__(self, font: pygame.font.Font, status_font: pygame.font.Font) -> None:
        self.font = font
        self.status_font = status_font

    def draw_workspace(self, surface: pygame.Surface, client: pygame.Rect, page_rect: pygame.Rect) -> None:
        """Render workspace backdrop and simulated paper surface with drop shadow."""
        pygame.draw.rect(surface, (215, 218, 224), client)
        shadow_rect = pygame.Rect(
            page_rect.x + 3, page_rect.y + 3, page_rect.width, page_rect.height
        )
        pygame.draw.rect(surface, (170, 175, 185), shadow_rect)
        pygame.draw.rect(surface, (255, 255, 255), page_rect)
        pygame.draw.rect(surface, (190, 195, 205), page_rect, 1)

    def draw_content(
        self,
        surface: pygame.Surface,
        page_rect: pygame.Rect,
        visual_lines: List[Dict[str, Any]],
        scroll_y: int,
        cursor_v_idx: int,
        cursor_x_off: int,
        cursor_visible: bool,
        is_active: bool,
        line_height: int = 26,
        padding_x: int = 20,
        padding_y: int = 15,
    ) -> None:
        """Render visible text lines, line rules, selection highlights, and blinking cursor."""
        visible_lines_count = max(1, (page_rect.height - (padding_y * 2)) // line_height)
        start_index = max(0, scroll_y)
        end_index = min(len(visual_lines), start_index + visible_lines_count + 1)

        base_x = page_rect.x + padding_x
        base_y = page_rect.y + padding_y

        for idx in range(start_index, end_index):
            vline = visual_lines[idx]
            render_y = base_y + (idx - scroll_y) * line_height

            # Line guide rule
            guide_y = render_y + line_height - 2
            pygame.draw.line(
                surface,
                (230, 230, 230),
                (base_x - 5, guide_y),
                (page_rect.x + page_rect.width - padding_x + 5, guide_y),
                1,
            )

            # Active line highlight
            if idx == cursor_v_idx and is_active:
                h_rect = pygame.Rect(
                    base_x - 5,
                    render_y,
                    page_rect.width - (padding_x * 2) + 10,
                    line_height,
                )
                pygame.draw.rect(surface, (235, 243, 250), h_rect)

            # Text
            if vline["text"]:
                img = self.font.render(vline["text"], True, (0, 0, 0))
                surface.blit(img, (base_x, render_y))

        # Active cursor line bar
        if cursor_visible and is_active and (start_index <= cursor_v_idx < end_index):
            cursor_y = base_y + (cursor_v_idx - scroll_y) * line_height
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (base_x + cursor_x_off, cursor_y + 2, 2, line_height - 4),
            )

    def draw_statusbar(
        self,
        surface: pygame.Surface,
        client: pygame.Rect,
        file_name: str,
        is_dirty: bool,
        row: int,
        col: int,
        word_count: int,
        height: int = 24,
    ) -> None:
        """Render status indicator bar at the bottom of the client window."""
        status_rect = pygame.Rect(
            client.x,
            client.y + client.height - height,
            client.width,
            height,
        )
        pygame.draw.rect(surface, (235, 238, 242), status_rect)
        pygame.draw.line(
            surface,
            (200, 205, 215),
            (status_rect.x, status_rect.y),
            (status_rect.x + status_rect.width, status_rect.y),
        )

        dirty_flag = "*" if is_dirty else ""
        text = f" {file_name}{dirty_flag} | Line {row + 1}, Col {col + 1} | Words: {word_count} | 100%"
        status_surf = self.status_font.render(text, True, (80, 85, 95))
        surface.blit(status_surf, (status_rect.x + 10, status_rect.y + 3))