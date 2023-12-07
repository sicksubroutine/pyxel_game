# Where assets are stored
import pyxel as px
import glm
from misc.entity import EntityPool
from components.sprite import Sprite, SpriteLayer
from components.transform import Transform
from misc.logger import Logger


class AssetStore:
    def __init__(self, logger: Logger) -> None:
        self.assets = {}
        self.fonts = {}
        self.sounds = {}
        self.logger = logger
        self.logger.Log("Asset Store created")

    def clear_assets(self) -> None:
        for asset in self.assets:
            asset = None
        self.assets.clear()
        for sound in self.sounds:
            sound = None
        self.sounds.clear()

    def load_resource(self, name, file_path) -> None:
        px.load(file_path)
        self.logger.Log(f"Loaded resource {name} from {file_path}")

    def add_texture(self, name, file_path) -> None:
        self.assets[name] = px.Image.load(file_path)

    def get_texture(self, name) -> px.Image:
        return self.assets[name]

    def add_sound(self, name, file_path) -> None:
        self.sounds[name] = px.Sound(file_path)

    def get_sound(self, name) -> px.Sound:
        return self.sounds[name]
