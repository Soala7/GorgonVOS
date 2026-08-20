from resources.paths import ICONS

class IconManager:

    def __init__(self, assets):
        self.assets = assets

    def app(self, filename):
        return self.assets.load_image(ICONS / "apps" / filename)

    def system(self, filename):
        return self.assets.load_image(ICONS / "system" / filename)

    def folder(self, filename):
        return self.assets.load_image(ICONS / "folders" / filename)

    def file(self, filename):
        return self.assets.load_image(ICONS / "files" / filename)

    def status(self, filename):
        return self.assets.load_image(ICONS / "status" / filename)

    def explorer_tool(self, filename):
        return self.assets.load_image(ICONS / "apps" / "explorer_tools" / filename)
