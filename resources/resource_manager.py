from resources.asset_manager import AssetManager
from resources.font_manager import FontManager
from resources.icon_manager import IconManager
from resources.sound_manager import SoundManager
from resources.theme_manager import ThemeManager


class ResourceManager:
    #Central access point for every resource in VOS.
    def __init__(self):

        self.assets = AssetManager()

        self.fonts = FontManager()

        self.sounds = SoundManager()

        self.theme = ThemeManager()

        self.icons = IconManager(self.assets)