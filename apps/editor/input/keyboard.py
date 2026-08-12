"""
Gorgon OS (VOS)

Editor Keyboard Handler
-----------------------
Handles keyboard input and shortcuts for the text editor.

This module does not draw anything and does not know about
the editor window's UI.

It delegates document changes to the document and cursor
objects.
"""

from __future__ import annotations

import pygame


class EditorKeyboardHandler:
    """
    Processes keyboard events for the editor.

    Expected objects:

        document
            Handles text content.

        cursor
            Handles cursor position.

        clipboard
            Optional clipboard implementation.

    The handler returns True when it consumes an event.
    """

    def __init__(
        self,
        document,
        cursor,
        clipboard=None,
    ) -> None:

        self.document = document
        self.cursor = cursor
        self.clipboard = clipboard

    # --------------------------------------------------
    # Main Event Handler
    # --------------------------------------------------

    def handle(self, event) -> bool:
        """
        Process a keyboard event.

        Returns True if the event was handled.
        """

        if not hasattr(event, "key"):
            return False

        key = event.key

        # ----------------------------------------------
        # Ctrl shortcuts
        # ----------------------------------------------

        mods = getattr(
            event,
            "mod",
            pygame.key.get_mods(),
        )

        if mods & pygame.KMOD_CTRL:

            if self._handle_shortcut(key):
                return True

        # ----------------------------------------------
        # Editing
        # ----------------------------------------------

        if key == pygame.K_BACKSPACE:

            self.cursor.backspace(
                self.document
            )

            return True

        if key == pygame.K_DELETE:

            self.cursor.delete_forward(
                self.document
            )

            return True

        if key == pygame.K_RETURN:

            self.cursor.insert_newline(
                self.document
            )

            return True

        # ----------------------------------------------
        # Cursor movement
        # ----------------------------------------------

        if key == pygame.K_LEFT:

            self.cursor.left(
                self.document
            )

            return True

        if key == pygame.K_RIGHT:

            self.cursor.right(
                self.document
            )

            return True

        if key == pygame.K_UP:

            self.cursor.up(
                self.document
            )

            return True

        if key == pygame.K_DOWN:

            self.cursor.down(
                self.document
            )

            return True

        # ----------------------------------------------
        # Printable character
        # ----------------------------------------------

        unicode_text = getattr(
            event,
            "unicode",
            "",
        )

        if (
            unicode_text
            and unicode_text.isprintable()
        ):

            self.cursor.insert_text(
                self.document,
                unicode_text,
            )

            return True

        return False

    # --------------------------------------------------
    # Shortcuts
    # --------------------------------------------------

    def _handle_shortcut(
        self,
        key,
    ) -> bool:
        """
        Handles Ctrl-based shortcuts.

        Returns True if the shortcut was consumed.
        """

        # Ctrl+C
        if key == pygame.K_c:

            self.copy()

            return True

        # Ctrl+V
        if key == pygame.K_v:

            self.paste()

            return True

        # Ctrl+X
        if key == pygame.K_x:

            self.cut()

            return True

        # Ctrl+A
        if key == pygame.K_a:

            self.select_all()

            return True

        # Ctrl+S
        #
        # Saving is deliberately handled by the
        # editor/window layer later.
        #
        # Returning a special action would be better
        # than making this class know about FileService.
        if key == pygame.K_s:

            return False

        return False

    # --------------------------------------------------
    # Clipboard
    # --------------------------------------------------

    def copy(self) -> None:
        """
        Copy the current selection.

        Selection support will be connected once the
        Cursor/Document classes support selections.
        """

        if self.clipboard is not None:
            self.clipboard.copy(
                self.document,
                self.cursor,
            )

    # --------------------------------------------------

    def paste(self) -> None:
        """
        Paste clipboard text.
        """

        if self.clipboard is not None:
            self.clipboard.paste(
                self.document,
                self.cursor,
            )

    # --------------------------------------------------

    def cut(self) -> None:
        """
        Cut the current selection.
        """

        if self.clipboard is not None:
            self.clipboard.cut(
                self.document,
                self.cursor,
            )

    # --------------------------------------------------

    def select_all(self) -> None:
        """
        Select the entire document.

        Selection support will be connected later.
        """

        if hasattr(
            self.cursor,
            "select_all",
        ):

            self.cursor.select_all(
                self.document
            )