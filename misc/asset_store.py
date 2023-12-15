# Where assets are stored
import pyxel as px
from misc.logger import Logger
from components.audio import Sound


class AssetStore:
    def __init__(self, logger: Logger) -> None:
        self.sounds = {}
        self.resources = {}
        self.logger = logger
        self.logger.Log("Asset Store created")

    def clear_assets(self) -> None:
        for asset in self.resources:
            asset = None
        self.resources.clear()
        for sound in self.sounds:
            sound = None
        self.sounds.clear()

    def load_resource(self, name, file_path) -> None:
        self.resources[name] = {
            "name": name,
            "file_path": file_path,
        }
        px.load(file_path)
        self.logger.Log(f"Loaded resource {name} from {file_path}")

    def add_sound(self, name: str) -> None:
        self.sounds[name] = int(Sound())
        self.logger.Log(f"Added sound {name}")
        return self.sounds[name]

    def get_sound(self, name) -> int:
        return self.sounds[name]
