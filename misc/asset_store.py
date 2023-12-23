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

    def check_resource(self, name) -> bool:
        if name not in self.resources:
            self.logger.Err(f"Resource {name} does not exist")
            return False
        return True

    def load_resource(self, name, file_path) -> None:
        self.resources[name] = {
            "name": name,
            "file_path": file_path,
        }
        px.load(file_path)
        self.logger.Log(f"Loaded resource {name} from {file_path}")

    def check_sound(self, name) -> bool:
        if name not in self.sounds:
            self.logger.Err(f"Sound {name} does not exist")
            return False
        return True

    def add_sound(self, name: str) -> None:
        self.sounds[name] = int(Sound())
        self.logger.Log(f"Added sound {name}")
        return self.sounds[name]

    def get_sound(self, name) -> int:
        if name not in self.sounds:
            self.logger.Err(f"Sound {name} does not exist")
            return -1
        return self.sounds[name]
