import pygame

from resources.cache import ResourceCache
from resources.paths import (
    BOOT,
    CURSORS,
    ICONS,
    WALLPAPERS,
)

class AssetManager:

    def __init__(self):
        self.cache = ResourceCache()

    def load_image(self, path):
        path = str(path)
        if path not in self.cache.images:
            self.cache.images[path] = pygame.image.load(path).convert_alpha()

        return self.cache.images[path]

    def boot_image(self, filename):
        return self.load_image(BOOT / filename)

    def cursor(self, filename):
        return self.load_image(CURSORS / filename)

    def wallpaper(self, filename):
        return self.load_image(WALLPAPERS / filename)

    def icon(self, category, filename):
        return self.load_image(ICONS / category / filename)

    def clear_cache(self):
        self.cache.clear()
