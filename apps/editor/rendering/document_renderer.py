"""
Gorgon OS (VOS)

Document Renderer
-----------------
Handles visual rendering for the text editor.

This module draws:
    - Editor workspace
    - Document page
    - Page shadow
    - Text
    - Ruled lines
    - Active-line highlight
    - Cursor
    - Status bar
"""

from __future__ import annotations

import pygame

from apps.editor.rendering.editor_layout import EditorLayout


class DocumentRenderer:
    """
    Responsible only for drawing the editor document.

    It does not:
        - modify document content
        - move the cursor
        - handle keyboard input
        - save files
    """

    def __init__(
        self,
        font: pygame.font.Font,
        status_font: pygame.font.Font,
    ) -> None:

        self.font = font
        self.status_font = status_font

        self.workspace_color = (215, 218, 224)
        self.page_color = (255, 255, 255)
        self.page_border_color = (190, 195, 205)
        self.shadow_color = (170, 175, 185)

        self.text_color = (0, 0, 0)
        self.cursor_color = (0, 0, 0)

        self.line_color = (0, 0, 0)
        self.highlight_color = (235, 243, 250)

        self.status_color = (235, 238, 242)
        self.status_border_color = (200, 205, 215)
        self.status_text_color = (80, 85, 95)

    # --------------------------------------------------
    # Main Document Rendering
    # --------------------------------------------------

    def draw_document(
        self,
        surface: pygame.Surface,
        client: pygame.Rect,
        page_rect: pygame.Rect,
        layout: EditorLayout,
        lines: list[str],
        cursor_row: int,
        cursor_col: int,
        cursor_visible: bool,
        is_active: bool,
    ) -> None:

        self._draw_workspace(
            surface,
            client,
            page_rect,
        )

        self._draw_document_content(
            surface,
            page_rect,
            layout,
            cursor_row,
            cursor_col,
            cursor_visible,
            is_active,
        )

    # --------------------------------------------------
    # Workspace
    # --------------------------------------------------

    def _draw_workspace(
        self,
        surface: pygame.Surface,
        client: pygame.Rect,
        page_rect: pygame.Rect,
    ) -> None:

        pygame.draw.rect(
            surface,
            self.workspace_color,
            client,
        )

        shadow_rect = pygame.Rect(
            page_rect.x + 3,
            page_rect.y + 3,
            page_rect.width,
            page_rect.height,
        )

        pygame.draw.rect(
            surface,
            self.shadow_color,
            shadow_rect,
        )

        pygame.draw.rect(
            surface,
            self.page_color,
            page_rect,
        )

        pygame.draw.rect(
            surface,
            self.page_border_color,
            page_rect,
            1,
        )

    # --------------------------------------------------
    # Document Content
    # --------------------------------------------------

    def _draw_document_content(
        self,
        surface: pygame.Surface,
        page_rect: pygame.Rect,
        layout: EditorLayout,
        cursor_row: int,
        cursor_col: int,
        cursor_visible: bool,
        is_active: bool,
    ) -> None:

        start_index, end_index = (
            layout.get_visible_range(page_rect)
        )

        base_x, base_y = (
            layout.get_text_origin(page_rect)
        )

        cursor_v_idx, cursor_x = (
            layout.get_cursor_visual_info(
                cursor_row,
                cursor_col,
            )
        )

        for index in range(
            start_index,
            end_index,
        ):

            visual = layout.visual_lines[index]

            render_y = (
                base_y
                + (index - layout.scroll_y)
                * layout.line_height
            )

            # ------------------------------------------
            # Active line
            # ------------------------------------------

            if (
                index == cursor_v_idx
                and is_active
            ):

                highlight_rect = pygame.Rect(
                    base_x - 5,
                    render_y,
                    page_rect.width
                    - layout.page_padding_x * 2
                    + 10,
                    layout.line_height,
                )

                pygame.draw.rect(
                    surface,
                    self.highlight_color,
                    highlight_rect,
                )

            # ------------------------------------------
            # Ruled line
            # ------------------------------------------

            guide_y = (
                render_y
                + layout.line_height
                - 2
            )

            pygame.draw.line(
                surface,
                self.line_color,
                (
                    base_x - 5,
                    guide_y,
                ),
                (
                    page_rect.right
                    - layout.page_padding_x
                    + 5,
                    guide_y,
                ),
                2,
            )

            # ------------------------------------------
            # Text
            # ------------------------------------------

            text_surface = self.font.render(
                visual.text,
                True,
                self.text_color,
            )

            surface.blit(
                text_surface,
                (
                    base_x,
                    render_y,
                ),
            )

        # ----------------------------------------------
        # Cursor
        # ----------------------------------------------

        if (
            cursor_visible
            and is_active
            and start_index
            <= cursor_v_idx
            < end_index
        ):

            cursor_y = (
                base_y
                + (
                    cursor_v_idx
                    - layout.scroll_y
                )
                * layout.line_height
            )

            cursor_rect = pygame.Rect(
                base_x + cursor_x,
                cursor_y + 2,
                2,
                layout.line_height - 4,
            )

            pygame.draw.rect(
                surface,
                self.cursor_color,
                cursor_rect,
            )

    # --------------------------------------------------
    # Status Bar
    # --------------------------------------------------

    def draw_status_bar(
        self,
        surface: pygame.Surface,
        client: pygame.Rect,
        file_name: str,
        is_dirty: bool,
        cursor_row: int,
        cursor_col: int,
        lines: list[str],
    ) -> None:

        status_rect = pygame.Rect(
            client.x,
            client.bottom - 24,
            client.width,
            24,
        )

        pygame.draw.rect(
            surface,
            self.status_color,
            status_rect,
        )

        pygame.draw.line(
            surface,
            self.status_border_color,
            (
                status_rect.x,
                status_rect.y,
            ),
            (
                status_rect.right,
                status_rect.y,
            ),
        )

        word_count = sum(
            len(line.split())
            for line in lines
        )

        dirty_flag = "*" if is_dirty else ""

        status_text = (
            f" {file_name}{dirty_flag}"
            f" | Line {cursor_row + 1}"
            f", Col {cursor_col + 1}"
            f" | Words: {word_count}"
            f" | 100%"
        )

        status_surface = self.status_font.render(
            status_text,
            True,
            self.status_text_color,
        )

        surface.blit(
            status_surface,
            (
                status_rect.x + 10,
                status_rect.y + 3,
            ),
        )