import json

from resources.paths import THEMES

class ThemeManager:

    def __init__(self):
        self.theme = {}
        self.colors = {}

        self.load()

    def load(self):
        with open(THEMES / "theme.json", "r", encoding="utf-8") as file:
            self.theme = json.load(file)

        with open(THEMES / "colors.json", "r", encoding="utf-8") as file:
            self.colors = json.load(file)

    def get(self, key, default=None):
        return self.theme.get(key, default)

    def color(self, name, default=None):
        return self.colors.get(name, default)

    def reload(self):
        self.load()
