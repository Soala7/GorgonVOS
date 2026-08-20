import unittest
from unittest.mock import patch

import pygame

from desktop.shell.dock import Dock
from desktop.ui.core.event import KeyModifier, KeyReleaseEvent, MouseButton, MousePressEvent

class DockEventTests(unittest.TestCase):
    def test_dock_handles_ui_mouse_press(self):
        dock = Dock()
        dock.launcher_open = False

        with patch.object(pygame.display, "get_surface", return_value=pygame.Surface((1000, 800))):
            dock.handle_event(MousePressEvent(230, 700, MouseButton.LEFT))

        self.assertTrue(dock.launcher_open)

    def test_dock_ignores_key_release_events(self):
        dock = Dock()
        dock.launcher_open = False

        dock.handle_event(KeyReleaseEvent(13, KeyModifier.NONE))

        self.assertFalse(dock.launcher_open)

if __name__ == "__main__":
    unittest.main()
