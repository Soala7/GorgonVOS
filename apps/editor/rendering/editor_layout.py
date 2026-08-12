"""
Gorgon OS (VOS)

Editor Layout
-------------
Handles visual layout calculations for the text editor.

This module does NOT draw anything and does NOT modify the document.
It calculates:

    - Page dimensions
    - Text area dimensions
    - Word wrapping
    - Visual line positions
    - Cursor visual position
    - Mouse position -> document position
    - Scroll calculations
"""

from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class VisualLine:
    """
    Represents one visually rendered line.

    A single logical document line can produce
    multiple VisualLine objects because of wrapping.
    """

    row: int
    col_start: int
    text: str


class EditorLayout:
    """
    Calculates the visual layout of an editor document.

    The document itself is owned by EditorDocument.
    This class only calculates how that document
    should appear on screen.
    """

    def __init__(
        self,
        font: pygame.font.Font,
        page_padding_x: int = 20,
        page_padding_y: int = 15,
        line_height: int = 26,
        status_bar_height: int = 24,
    ) -> None:

        self.font = font

        self.page_padding_x = page_padding_x
        self.page_padding_y = page_padding_y
        self.line_height = line_height
        self.status_bar_height = status_bar_height

        self.visual_lines: list[VisualLine] = []

        self.scroll_y = 0

        self._last_width = -1
        self._needs_update = True

    # --------------------------------------------------
    # Invalidation
    # --------------------------------------------------

    def invalidate(self) -> None:
        """
        Forces the layout to be recalculated.
        """

        self._needs_update = True

    # --------------------------------------------------
    # Page Geometry
    # --------------------------------------------------

    def get_page_rect(self, client: pygame.Rect) -> pygame.Rect:
        """
        Returns the white document page inside the editor.
        """

        page_width = min(
            810,
            client.width - 20,
        )

        page_width = max(
            300,
            page_width,
        )

        page_height = (
            client.height
            - self.status_bar_height
            - 10
        )

        page_x = (
            client.x
            + (client.width - page_width) // 2
        )

        page_y = client.y + 5

        return pygame.Rect(
            page_x,
            page_y,
            page_width,
            page_height,
        )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    def update(
        self,
        lines: list[str],
        window_width: int,
    ) -> None:
        """
        Rebuilds the visual line layout.

        `lines` contains the logical document lines.

        The document itself is never modified.
        """

        if (
            not self._needs_update
            and window_width == self._last_width
        ):
            return

        self._last_width = window_width
        self._needs_update = False

        client_width = window_width - 4

        page_width = min(
            810,
            client_width - 20,
        )

        max_text_width = max(
            100,
            page_width
            - (self.page_padding_x * 2),
        )

        self.visual_lines.clear()

        for row, line in enumerate(lines):

            self._wrap_line(
                row,
                line,
                max_text_width,
            )

        self.scroll_y = min(
            self.scroll_y,
            max(0, len(self.visual_lines) - 1),
        )

    # --------------------------------------------------

    def _wrap_line(
        self,
        row: int,
        line: str,
        max_width: int,
    ) -> None:
        """
        Converts one logical line into one or more
        visual lines.
        """

        if not line:

            self.visual_lines.append(
                VisualLine(
                    row=row,
                    col_start=0,
                    text="",
                )
            )

            return

        words: list[str] = []
        word = ""

        for char in line:

            word += char

            if char in (" ", "-"):

                words.append(word)
                word = ""

        if word:
            words.append(word)

        current_text = ""
        start_col = 0

        for word in words:

            test_text = current_text + word

            # Normal wrapping
            if (
                self.font.size(test_text)[0] > max_width
                and current_text
            ):

                self.visual_lines.append(
                    VisualLine(
                        row=row,
                        col_start=start_col,
                        text=current_text,
                    )
                )

                start_col += len(current_text)
                current_text = word

            # Extremely long word
            elif (
                self.font.size(test_text)[0] > max_width
                and not current_text
            ):

                chunk = ""

                for char in word:

                    test_chunk = chunk + char

                    if (
                        self.font.size(test_chunk)[0]
                        > max_width
                        and chunk
                    ):

                        self.visual_lines.append(
                            VisualLine(
                                row=row,
                                col_start=start_col,
                                text=chunk,
                            )
                        )

                        start_col += len(chunk)
                        chunk = char

                    else:
                        chunk = test_chunk

                current_text = chunk

            else:

                current_text = test_text

        if current_text:

            self.visual_lines.append(
                VisualLine(
                    row=row,
                    col_start=start_col,
                    text=current_text,
                )
            )

    # --------------------------------------------------
    # Cursor
    # --------------------------------------------------

    def get_cursor_visual_info(
        self,
        cursor_row: int,
        cursor_col: int,
    ) -> tuple[int, int]:
        """
        Returns:

            (visual_line_index, cursor_x_offset)
        """

        if not self.visual_lines:
            return 0, 0

        for index, visual in enumerate(
            self.visual_lines
        ):

            if visual.row != cursor_row:
                continue

            start = visual.col_start
            end = start + len(visual.text)

            is_last_chunk = True

            if index + 1 < len(self.visual_lines):

                next_line = self.visual_lines[index + 1]

                if next_line.row == cursor_row:
                    is_last_chunk = False

            # Cursor inside this visual line
            if start <= cursor_col < end:

                relative_col = (
                    cursor_col - start
                )

                x_offset = self.font.size(
                    visual.text[:relative_col]
                )[0]

                return index, x_offset

            # Cursor at the end of the final wrapped line
            if (
                is_last_chunk
                and cursor_col >= end
            ):

                x_offset = self.font.size(
                    visual.text
                )[0]

                return index, x_offset

        return 0, 0

    # --------------------------------------------------
    # Mouse -> Cursor
    # --------------------------------------------------

    def get_column_from_x(
        self,
        text: str,
        target_x: int,
    ) -> int:
        """
        Converts a mouse X position into the
        closest character position.
        """

        best_col = 0
        smallest_distance = float("inf")

        for col in range(len(text) + 1):

            x = self.font.size(
                text[:col]
            )[0]

            distance = abs(
                x - target_x
            )

            if distance < smallest_distance:

                smallest_distance = distance
                best_col = col

        return best_col

    # --------------------------------------------------
    # Scrolling
    # --------------------------------------------------

    def scroll(
        self,
        amount: int,
    ) -> None:
        """
        Scrolls the visual document.
        """

        maximum = max(
            0,
            len(self.visual_lines) - 1,
        )

        self.scroll_y += amount

        self.scroll_y = max(
            0,
            min(
                self.scroll_y,
                maximum,
            ),
        )

    # --------------------------------------------------

    def ensure_cursor_visible(
        self,
        cursor_row: int,
        cursor_col: int,
        window_height: int,
    ) -> None:
        """
        Automatically scrolls the document so the
        cursor remains visible.
        """

        visual_index, _ = (
            self.get_cursor_visual_info(
                cursor_row,
                cursor_col,
            )
        )

        client_height = (
            window_height
            - 64
        )

        visible_lines = max(
            1,
            (
                client_height
                - self.page_padding_y * 2
            )
            // self.line_height,
        )

        if visual_index < self.scroll_y:

            self.scroll_y = visual_index

        elif (
            visual_index
            >= self.scroll_y + visible_lines
        ):

            self.scroll_y = (
                visual_index
                - visible_lines
                + 1
            )

    # --------------------------------------------------
    # Visible Lines
    # --------------------------------------------------

    def get_visible_range(
        self,
        page_rect: pygame.Rect,
    ) -> tuple[int, int]:
        """
        Returns the visual-line indexes that should
        currently be rendered.
        """

        visible_lines = max(
            1,
            (
                page_rect.height
                - self.page_padding_y * 2
            )
            // self.line_height,
        )

        start = max(
            0,
            self.scroll_y,
        )

        end = min(
            len(self.visual_lines),
            start + visible_lines + 1,
        )

        return start, end

    # --------------------------------------------------
    # Coordinates
    # --------------------------------------------------

    def get_text_origin(
        self,
        page_rect: pygame.Rect,
    ) -> tuple[int, int]:
        """
        Returns the X/Y coordinate where document
        text begins.
        """

        return (
            page_rect.x
            + self.page_padding_x,

            page_rect.y
            + self.page_padding_y,
        )