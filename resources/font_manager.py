import pygame

from resources.cache import ResourceCache
from resources.paths import FONTS

class FontManager:

    def __init__(self):
        self.cache = ResourceCache()

    def load(self, filename: str, size: int):
        key = (filename, size)

        if key not in self.cache.fonts:
            path = FONTS / filename
            self.cache.fonts[key] = pygame.font.Font(str(path), size)

        return self.cache.fonts[key]

    def clear(self):
        self.cache.fonts.clear()
