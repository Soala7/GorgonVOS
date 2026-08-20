import pygame

from resources.cache import ResourceCache
from resources.paths import SOUNDS

class SoundManager:

    def __init__(self):
        self.cache = ResourceCache()

    def load(self, filename: str):
        if filename not in self.cache.sounds:
            path = SOUNDS / filename
            self.cache.sounds[filename] = pygame.mixer.Sound(str(path))

        return self.cache.sounds[filename]

    def play(self, filename: str):
        self.load(filename).play()

    def stop(self, filename: str):
        self.load(filename).stop()

    def clear(self):
        self.cache.sounds.clear()
