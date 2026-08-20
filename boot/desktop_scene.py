"""
Gorgon OS (VOS)

Desktop Scene
"""

from __future__ import annotations

from desktop.shell.shell import Shell

class DesktopScene:
    """
    Main desktop scene.
    """

    def __init__(self) -> None:

        self.shell = Shell()

    def update(
        self,
        dt: float,
    ) -> None:

        self.shell.update(dt)

    def draw(
        self,
        renderer,
    ) -> None:

        self.shell.draw(renderer)

    def handle_event(
        self,
        event,
    ) -> None:

        self.shell.handle_event(event)
