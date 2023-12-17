import esper as es
from misc.logger import Logger
from misc.asset_store import AssetStore
from misc.entity import EntityPool

from systems.player_system import PlayerSystem
from level_loader.enemies import Enemies
from level_loader.level1 import Level1


class MissingComponent(Exception):
    pass


class LevelLoader:
    def __init__(self, game, default_level=1):
        self.game = game
        self.logger: Logger = game.logger
        self.asset_store: AssetStore = game.asset_store
        self.pool: EntityPool = game.pool
        self.player_system: PlayerSystem = game.player_system
        self.enemies: Enemies = Enemies(self.game)
        self.current_level = default_level
        self.levels = {
            0: {"name": "level0", "class": None},
            1: {"name": "Level 1", "class": Level1},
        }
        es.switch_world(self.levels[self.current_level]["name"])
        if "default" in es.list_worlds():
            es.delete_world("default")

        self.possible_components = self.pool.possible_components
        self.load_level()
        self.delay = 0

    def class_checker(self):
        self.assets_present = False
        self.player_present = False
        self.menu_present = False
        self.entities_present = False
        self.spawn_schedule_present = False
        level_name = self.levels[self.current_level]["name"]

        if hasattr(self.loaded_level, "assets"):
            self.logger.Log(f"Loading assets for {level_name}...")
            self.assets_present = True
        if hasattr(self.loaded_level, "player"):
            self.logger.Log(f"Loading player for {level_name}...")
            self.player_present = True
        if hasattr(self.loaded_level, "menu"):
            self.logger.Log(f"Loading menus for {level_name}...")
            self.menu_present = True
        if hasattr(self.loaded_level, "entities"):
            self.logger.Log(f"Loading entities for {level_name}...")
            self.entities_present = True
        if hasattr(self.loaded_level, "spawn_schedule"):
            self.logger.Log(f"Loading spawn schedule for {level_name}...")
            self.spawn_schedule_present = True

    def load_level_class(self, level_name):
        try:
            if level_name not in self.levels.values():
                self.logger.Warn(f"Level {level_name} not found")
                return
            level_class = level_name["class"]
            return level_class(self.game)
        except Exception as e:
            self.logger.Error(f"Error loading level {level_name}: {e}")

    def load_level(self):
        self.loaded_level = self.load_level_class(self.levels[self.current_level])
        self.logger.Log(f"Loading level {self.levels[self.current_level]['name']}...")
        self.class_checker()
        self.load_assets()
        self.load_player()

    def load_assets(self):
        if not self.assets_present:
            self.logger.Warn(f"No assets found for {self.levels[self.current_level]}")
            return
        for asset in self.loaded_level.assets:
            if asset["asset_type"] == "resource":
                self.asset_store.load_resource(asset["asset_id"], asset["path"])
            elif asset["asset_type"] == "sound":
                assigned_number = self.asset_store.add_sound(asset["asset_id"])
                assert (
                    assigned_number == asset["number"]
                ), f"Sound number {assigned_number} does not match {asset['number']}"

    def load_player(self):
        if not self.player_present:
            self.logger.Warn(f"No player found for {self.levels[self.current_level]}")
            return
        try:
            for component in self.loaded_level.player:
                if component.__class__ not in self.possible_components:
                    self.logger.Warn(
                        f"Component {component.__class__} not found in possible components"
                    )
                    raise MissingComponent("Missing component!")
        except MissingComponent as e:
            self.logger.Error(f"An issue with components was found: {e}")
            return
        components = [component for component in self.loaded_level.player]
        self.player = self.pool.create_entity(*components)

    def spawn_schedule(self):
        self.delay += 1
        enemies = self.loaded_level.spawn_schedule
        for enemy in enemies:
            if self.delay < enemy["delay"]:
                return
            self.logger.Log(f"Spawning {enemy['enemy']} at {enemy['x']}, {enemy['y']}")
            self.enemies.get_enemy(
                enemy["enemy"], enemy["x"], enemy["y"], enemy["health"]
            )
            enemies.remove(enemy)
