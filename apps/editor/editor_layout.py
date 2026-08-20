# editor_layout.py
from __future__ import annotations
import pygame
from typing import List, Dict, Tuple, Any


class EditorLayout:
    """Handles text wrapping geometry, viewport calculations, and cursor coordinates."""

    def __init__(self, font: pygame.font.Font, page_padding_x: int = 20, line_height: int = 26) -> None:
        self.font = font
        self.page_padding_x = page_padding_x
        self.line_height = line_height
        self.visual_lines: List[Dict[str, Any]] = []
        self._last_width: int = -1

    def update_layout(self, lines: List[str], window_width: int, max_page_w: int = 810) -> None:
        """Recalculate visual wrapped lines based on window width."""
        client_w = window_width - 4
        page_w = min(max_page_w, client_w - 20)
        max_text_width = max(100, page_w - (self.page_padding_x * 2))

        self.visual_lines = []
        for row_idx, line in enumerate(lines):
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
                while self.font.size(w)[0] > max_text_width:
                    for i in range(1, len(w)):
                        if self.font.size(w[:i])[0] > max_text_width:
                            chunk = w[: i - 1]
                            self.visual_lines.append(
                                {"row": row_idx, "col_start": start_idx, "text": chunk}
                            )
                            start_idx += len(chunk)
                            w = w[i - 1 :]
                            break

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

    def get_cursor_visual_info(self, cursor_row: int, cursor_col: int) -> Tuple[int, int]:
        """Convert logical buffer row and col into visual line index and X pixel offset."""
        if not self.visual_lines:
            return 0, 0

        for i, vline in enumerate(self.visual_lines):
            if vline["row"] != cursor_row:
                continue

            end_col = vline["col_start"] + len(vline["text"])
            is_last_chunk = True
            if i + 1 < len(self.visual_lines) and self.visual_lines[i + 1]["row"] == cursor_row:
                is_last_chunk = False

            if vline["col_start"] <= cursor_col < end_col:
                rel_col = cursor_col - vline["col_start"]
                return i, self.font.size(vline["text"][:rel_col])[0]
            elif is_last_chunk and cursor_col >= end_col:
                return i, self.font.size(vline["text"])[0]

        return 0, 0

    def get_col_from_x_offset(self, text: str, target_x: float) -> int:
        """Find closest character column index for a given horizontal pixel offset."""
        best_col, min_dist = 0, float("inf")
        for col in range(len(text) + 1):
            dist = abs(self.font.size(text[:col])[0] - target_x)
            if dist < min_dist:
                min_dist, best_col = dist, col
            elif dist > min_dist:
                break
        return best_col

      

       