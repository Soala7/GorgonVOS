class ResourceCache:

    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.sounds = {}

    def clear(self):
        self.images.clear()
        self.fonts.clear()
        self.sounds.clear()
