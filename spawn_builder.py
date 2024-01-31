"""
A tool for building a Spawn Schedule that each level will contain.
It will be a graphical interface that will allow the user to place enemies depending on the "timer" of the level.

"""

import pyxel as px
import time
from glm import vec2
from misc.config import ConfigManager
from misc.logger import Logger
from misc.asset_store import AssetStore
from misc.entity import EntityPool
from dataclasses import dataclass

from level_loader.enemies import Enemies

from systems.star_system import StarSystem


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int


class BaseMode:
    def __init__(self, tool):
        self.tool = tool

    def render(self): ...

    def update(self): ...


class SelectionMode(BaseMode):
    def __init__(self, tool):
        self.tool = tool
        self.potential_ships = self.tool.potential_ships
        self.selected_ship = tool.selected_ship

    def render(self):
        px.text(0, 0, "Selection Mode", 7)
        for index, ship in enumerate(self.potential_ships):
            px.blt(
                10,
                10 + (10 * index),
                0,
                self.potential_ships[ship]["u"],
                self.potential_ships[ship]["v"],
                8,
                8,
                0,
            )

    def update(self):
        mouse_pos = vec2(px.mouse_x, px.mouse_y)
        if px.btnp(px.MOUSE_BUTTON_LEFT):
            for ship in self.potential_ships:
                if (
                    self.potential_ships[ship]["location_on_screen"].x
                    < mouse_pos.x
                    < self.potential_ships[ship]["location_on_screen"].x
                    + self.potential_ships[ship]["location_on_screen"].w
                    and self.potential_ships[ship]["location_on_screen"].y
                    < mouse_pos.y
                    < self.potential_ships[ship]["location_on_screen"].y
                    + self.potential_ships[ship]["location_on_screen"].h
                ):
                    print(f"Selected ship: {ship}")
                    self.tool.selected_ship = ship
                    self.tool.logger.Log(f"Selected ship: {self.selected_ship}")


class PlacementMode(BaseMode):
    def __init__(self, tool):
        self.tool = tool
        self.potential_ships = self.tool.potential_ships
        self.selected_ship = tool.selected_ship

    def render(self):
        px.text(0, 0, "Placement Mode", 7)
        for index, ship in enumerate(self.potential_ships):
            px.blt(
                10,
                10 + (10 * index),
                0,
                self.potential_ships[ship]["u"],
                self.potential_ships[ship]["v"],
                8,
                8,
                0,
            )

    def update(self): ...


class PreviewMode(BaseMode):
    def __init__(self, tool):
        self.tool = tool

    def render(self):
        px.text(0, 0, "Preview Mode", 7)

    def update(self): ...


class Spawner:
    """Use this to create enemies for the Spawn Builder"""

    def __init__(self, tool):
        self.tool = tool
        self.logger: Logger = tool.logger

    def gen_enemy(self, enemy): ...


class SpawnBuilder:
    def __init__(self):
        self.config: ConfigManager = ConfigManager()
        self.logger: Logger = Logger(
            console_print=False,
            file_write=True,
            file_path="spawn_builder.txt",
        )
        self.asset_store: AssetStore = AssetStore(self)
        self.spawner = Spawner(self)
        self.enemies: Enemies = Enemies(self)
        self.pool: EntityPool = EntityPool(self)
        self.selected_ship = None

        self.potential_ships = {
            "ship1": {"u": 8, "v": 0, "location_on_screen": Rect(10, 10, 8, 8)},
            "ship2": {"u": 8, "v": 8, "location_on_screen": Rect(10, 20, 8, 8)},
            "ship3": {"u": 8, "v": 16, "location_on_screen": Rect(10, 30, 8, 8)},
            "ship4": {"u": 8, "v": 24, "location_on_screen": Rect(10, 40, 8, 8)},
            "ship5": {"u": 8, "v": 32, "location_on_screen": Rect(10, 50, 8, 8)},
        }

        self.enemy_types = self.enemies.enemy_types

        self.res_width = self.config.window_width
        self.res_height = self.config.window_height
        self.fps = self.config.target_fps
        px.init(self.res_width, self.res_height, title="Spawn Builder", fps=self.fps)
        px.load("assets/assets.pyxres", True, True, True, True)
        self.logger.Log(f"Pyxel initialized at {self.res_width}x{self.res_height}")

        self.systems_setup()
        self.delay = 0.0

        # show mouse
        px.mouse(True)

        # possible modes: placement, preview
        self.possible_modes = [
            {
                "name": "selection",
                "class": SelectionMode,
            },
            {
                "name": "placement",
                "class": PlacementMode,
            },
            {
                "name": "preview",
                "class": PreviewMode,
            },
        ]
        self.mode_index = 0
        self.tool_mode = self.possible_modes[self.mode_index]
        self.tool_class = self.possible_modes[self.mode_index]["class"](self)

    def mode_class_switch(self):
        self.tool_mode = self.possible_modes[self.mode_index]
        self.tool_class = self.possible_modes[self.mode_index]["class"](self)

    def mode_switcher(self):
        # change mode class
        try:
            self.mode_index += 1
            if self.mode_index > len(self.possible_modes) - 1:
                self.mode_index = 0
        except Exception as e:
            self.logger.Log(f"Error: {e}")

    def keyboard_controls(self):
        # switch mode using m key
        if px.btnp(px.KEY_M):
            self.mode_switcher()
        # print out the current selected ship if press p
        if px.btnp(px.KEY_P):
            print(f"Selected ship: {self.selected_ship}")

    def mouse_controls(self):
        self.mouse_pos = vec2(px.mouse_x, px.mouse_y)
        # # center mouse on screen
        # px.mouse_x = self.res_width // 2
        # px.mouse_y = self.res_height // 2

    def fps_counter(self):
        self.frames += 1
        new_now = time.perf_counter()
        if new_now - self.last_clock >= 1.0:
            self.fps = round(self.frames / (new_now - self.last_clock), 2)
            self.frames = 0
            self.last_clock = new_now

    def systems_setup(self):
        star_colors = {
            "fastest_stars": "WHITE",
            "fast_stars": "LIGHT_BLUE",
            "slow_stars": "GRAY",
            "slowest_stars": "DARK_BLUE",
        }
        self.star_system = StarSystem(star_colors)

    def update(self):
        self.current_mode_update = self.tool_class.update()
        self.mode_class_switch()
        self.star_system.update()
        # self.mouse_controls()
        self.keyboard_controls()

    def render(self):
        px.cls(0)
        self.star_system.render()
        # print the current mode on the screen
        self.current_mode_render = self.tool_class.render()

    def run(self):
        px.run(self.update, self.render)


if __name__ == "__main__":
    sb = SpawnBuilder()
    sb.run()
