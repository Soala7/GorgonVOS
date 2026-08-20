import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import pygame

from desktop.assests.icon_manager import IconManager

class IconManagerTests(unittest.TestCase):
    def test_get_returns_none_for_invalid_svg(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "launcher").mkdir()
            (root / "launcher" / "snake.svg").write_text("not valid svg", encoding="utf-8")

            with patch.object(IconManager, "ROOT", root):
                self.assertIsNone(IconManager.get("launcher/snake", 32))

    def test_get_loads_png_stored_as_svg(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "launcher").mkdir()
            surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            surface.fill((255, 0, 0, 255))
            buffer = BytesIO()
            pygame.image.save(surface, buffer)
            png_bytes = buffer.getvalue()
            with open(root / "launcher" / "snake.svg", "wb") as handle:
                handle.write(png_bytes)

            with patch.object(IconManager, "ROOT", root):
                surface = IconManager.get("launcher/snake", 32)

            self.assertIsNotNone(surface)

if __name__ == "__main__":
    unittest.main()
