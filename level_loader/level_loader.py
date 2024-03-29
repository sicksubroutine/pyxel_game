import esper as es
import glm
from misc.logger import Logger
from misc.asset_store import AssetStore
from misc.entity import EntityPool

from systems.player_system import PlayerSystem
from level_loader.enemies import Enemies
from level_loader.level1 import Level1
from level_loader.level2 import Level2
from level_loader.level3 import Level3
from level_loader.start_menu import StartMenu
from level_loader.settings_menu import SettingsMenu
from level_loader.settings_menu import FPSSelect, ResolutionSelect
from level_loader.ship_select import ShipSelect
from level_loader.transition import TransitionScreen


class MissingComponent(Exception):
    pass


class LevelLoader:
    def __init__(self, game, starting_level="Start Menu"):
        self.game = game
        self.logger: Logger = game.logger
        self.asset_store: AssetStore = game.asset_store
        self.pool: EntityPool = game.pool
        self.player_system: PlayerSystem = game.player_system
        self.enemies: Enemies = Enemies(self.game)
        self.current_level = starting_level
        self.levels = {
            "Start Menu": {"name": "Start Menu", "class": StartMenu},
            "Settings Menu": {"name": "Settings Menu", "class": SettingsMenu},
            "FPS Select": {"name": "FPS Select", "class": FPSSelect},
            "Resolution Select": {"name": "Res Select", "class": ResolutionSelect},
            "Ship Selection": {"name": "Ship Selection", "class": ShipSelect},
            "Level 1": {"name": "Level 1", "class": Level1},
            "Level 2": {"name": "Level 2", "class": Level2},
            "Level 3": {"name": "Level 3", "class": Level3},
        }
        es.switch_world(self.levels[self.current_level]["name"])
        if "default" in es.list_worlds():
            es.delete_world("default")
        if "empty" in es.list_worlds():
            es.delete_world("empty")
        self.possible_components = self.pool.possible_components
        self.load_level()
        self.delay = 0
        self.t_delay = 0

    def class_checker(self):
        self.assets_present = False
        self.player_present = False
        self.menu_present = False
        self.entities_present = False
        self.spawn_schedule_present = False
        self.star_colors_present = False
        level_name = self.levels[self.current_level]["name"]

        self.assets_check(level_name)
        self.player_check(level_name)
        self.menu_check(level_name)
        self.entities_check(level_name)
        self.spawn_schedule_check(level_name)
        self.star_colors_check(level_name)

    def assets_check(self, level_name):
        if hasattr(self.loaded_level, "assets"):
            if not self.loaded_level.assets:
                self.logger.Warn(f"No assets found for {level_name}")
                return
            self.logger.Log(f"Loading assets for {level_name}...")
            self.assets_present = True

    def player_check(self, level_name):
        if hasattr(self.loaded_level, "player"):
            if not self.loaded_level.player:
                self.logger.Warn(f"No player found for {level_name}")
                return
            self.logger.Log(f"Loading player for {level_name}...")
            self.player_present = True

    def menu_check(self, level_name):
        if hasattr(self.loaded_level, "menu"):
            if not self.loaded_level.menu:
                self.logger.Warn(f"No menu found for {level_name}")
                return
            self.logger.Log(f"Loading menus for {level_name}...")
            self.menu_present = True

    def entities_check(self, level_name):
        if hasattr(self.loaded_level, "entities"):
            if not self.loaded_level.entities:
                self.logger.Warn(f"No entities found for {level_name}")
                return
            self.logger.Log(f"Loading entities for {level_name}...")
            self.entities_present = True

    def spawn_schedule_check(self, level_name):
        if hasattr(self.loaded_level, "spawn_schedule"):
            if not self.loaded_level.spawn_schedule:
                self.logger.Warn(f"No spawn schedule found for {level_name}")
                return
            self.logger.Log(f"Loading spawn schedule for {level_name}...")
            self.spawn_schedule_present = True

    def star_colors_check(self, level_name):
        if hasattr(self.loaded_level, "star_colors"):
            if not self.loaded_level.star_colors:
                self.logger.Warn(f"No star colors found for {level_name}")
                return
            self.logger.Log(f"Loading star colors for {level_name}...")
            self.star_colors_present = True

    def load_level_class(self, level_name):
        try:
            if level_name not in self.levels.values():
                self.logger.Warn(f"Level {level_name} not found")
                return
            level_class = level_name["class"]
            return level_class(self.game)
        except Exception as e:
            self.logger.Err(f"Error loading level {level_name}: {e}")

    def load_level(self):
        self.delay = 0
        self.loaded_level = self.load_level_class(self.levels[self.current_level])
        self.logger.Log(f"Loading level {self.levels[self.current_level]['name']}...")
        self.class_checker()
        self.load_assets()
        self.load_player()
        self.load_menu()
        self.load_star_colors()

    def next_level(self):
        current_level = self.levels[self.current_level]["name"]
        level_number = int(current_level.split(" ")[1])
        level_number += 1
        if f"Level {level_number}" not in self.levels:
            self.logger.Log("No more levels found")
            return
        self.current_level = f"Level {level_number}"
        es.switch_world(self.levels[self.current_level]["name"])
        if current_level in es.list_worlds():
            es.delete_world(current_level)
        self.pool.clear_all_entities()
        self.game.level_init(self.current_level)

    def previous_level(self):
        current_level = self.levels[self.current_level]["name"]
        self.current_level -= 1
        es.switch_world(self.levels[self.current_level]["name"])
        if current_level in es.list_worlds():
            es.delete_world(current_level)
        self.pool.clear_all_entities()
        self.game.level_init(self.current_level)

    def load_specific_level(self, level_name, menu_change=False):
        current_level = self.levels[self.current_level]["name"]
        # determine if level_name is a string or an int
        if isinstance(level_name, str):
            for level in self.levels.values():
                if level["name"] == level_name:
                    self.current_level = level["name"]
                    break
        if not menu_change:
            self.pool.clear_all_entities()
            es.switch_world(self.levels[self.current_level]["name"])
            if current_level in es.list_worlds():
                es.delete_world(current_level)
        self.game.level_init(self.current_level)

    def load_assets(self):
        if not self.assets_present:
            return
        for asset in self.loaded_level.assets:
            if asset["asset_type"] == "resource":
                if not self.asset_store.check_resource(asset["asset_id"]):
                    self.asset_store.load_resource(asset["asset_id"], asset["path"])
            elif asset["asset_type"] == "sound":
                if not self.asset_store.check_sound(asset["asset_id"]):
                    self.asset_store.add_sound(asset["asset_id"])

    def load_player(self):
        if not self.player_present:
            self.logger.Log("No player found")
            return
        try:
            for component in self.loaded_level.player:
                if component.__class__ not in self.possible_components:
                    self.logger.Warn(
                        f"Component {component.__class__} not found in possible components"
                    )
                    raise MissingComponent("Missing component!")
        except MissingComponent as e:
            self.logger.Err(f"An issue with components was found: {e}")
            return
        components = [component for component in self.loaded_level.player]
        self.player = self.player_system.player_setup(*components)

    def load_star_colors(self):
        if not self.star_colors_present:
            return
        self.star_colors = self.loaded_level.star_colors

    def spawn_schedule(self):
        if not self.spawn_schedule_present:
            return
        self.delay += 1
        enemies = self.loaded_level.spawn_schedule
        zero_enemies = len(self.pool.get_group("enemies")) == 0
        delay_ended = self.delay > self.t_delay
        for e in enemies:
            if self.delay < e["delay"]:
                return
            self.enemies.get_enemy(e["enemy"], e["x"], e["y"], e["velocity"])
            enemies.remove(e)
            self.t_delay = e["delay"] + 1000
        if not enemies and zero_enemies and delay_ended and self.menu_present:
            self.logger.Log(f"All enemies spawned! Moving to {self.current_level}")
            self.next_level()
        elif not enemies and zero_enemies and not self.menu_present:
            self.load_menu(True)

    def load_menu(self, transition_screen=False):
        if not self.menu_present and not transition_screen:
            return
        self.menu_render = self.loaded_level.menu_render
        self.menu_update = self.loaded_level.menu_update
        if transition_screen:
            self.menu_present = True
            level_name = self.levels[self.current_level]["name"]
            transition = TransitionScreen(self.game, level_name)
            self.game.menu_render = transition.menu_render
            self.game.menu_update = transition.menu_update
