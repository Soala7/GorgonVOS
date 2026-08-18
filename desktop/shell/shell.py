"""
Gorgon OS (VOS)

Shell
"""

from __future__ import annotations

from desktop.renderer import renderer
from desktop.shell.desktop import Desktop
from apps.terminal.terminal import Terminal
from apps.explorer.explorer import Explorer
from apps.editor.editor import TextEditor


class Shell:
    """
    Main desktop shell.
    """

    def __init__(self, service_manager) -> None:

        self.desktop = Desktop()

        self.terminal = Terminal(service_manager)

        self.explorer = Explorer(self.desktop.window_manager)

        self.text_editor = TextEditor(service_manager)

        self.service_manager = service_manager

        self.terminal.window_manager = self.desktop.window_manager

        self.explorer.window_manager = self.desktop.window_manager

        self.text_editor.window_manager = self.desktop.window_manager

        # Give desktop components access
        self.desktop.dock.launcher = self.desktop.launcher
        self.desktop.dock.terminal = self.terminal
        self.desktop.dock.explorer = self.explorer
        self.desktop.dock.text_editor = self.text_editor

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update(self, dt: float) -> None:

        self.desktop.update(dt)

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

    def draw(self, renderer) -> None:

        self.desktop.draw(renderer)

    # --------------------------------------------------
    # Events
    # --------------------------------------------------

    def handle_event(self, event) -> None:

        self.desktop.handle_event(event)