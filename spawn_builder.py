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

from level_loader.enemies import Enemies

from systems.star_system import StarSystem


class BaseMode:
    def __init__(self, tool):
        self.tool = tool

    def render(self): ...

    def update(self): ...


class PlacementMode(BaseMode):
    def __init__(self, tool):
        self.tool = tool
        self.potential_ships = self.tool.potential_ships
        self.selected_ship = None

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

    def update(self):
        # check if ship is selected using mouse and location on screen
        for index, ship in enumerate(self.potential_ships):
            if (
                self.tool.mouse_pos.x
                > self.potential_ships[ship]["location_on_screen"].x
                and self.tool.mouse_pos.x
                < self.potential_ships[ship]["location_on_screen"].x + 8
                and self.tool.mouse_pos.y
                > self.potential_ships[ship]["location_on_screen"].y
                and self.tool.mouse_pos.y
                < self.potential_ships[ship]["location_on_screen"].y + 8
            ):
                self.selected_ship = ship
                print(f"Selected ship: {self.selected_ship}")
                break
            else:
                self.selected_ship = None


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

        self.potential_ships = {
            "ship1": {"u": 8, "v": 0, "location_on_screen": vec2(10, 10)},
            "ship2": {"u": 8, "v": 8, "location_on_screen": vec2(10, 20)},
            "ship3": {"u": 8, "v": 16, "location_on_screen": vec2(10, 30)},
            "ship4": {"u": 8, "v": 24, "location_on_screen": vec2(10, 40)},
            "ship5": {"u": 8, "v": 32, "location_on_screen": vec2(10, 50)},
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

        # possible modes: placement, preview
        self.possible_modes = ["placement", "preview"]
        self.tool_mode = self.possible_modes[0]  # Starting mode is placement

        self.placement_mode = PlacementMode(self)
        self.preview_mode = PreviewMode(self)
        self.tool_class = self.placement_mode

    def mode_switcher(self, current_mode):
        # change mode class
        try:
            if current_mode == self.possible_modes[0]:
                self.tool_class = self.placement_mode
            elif current_mode == self.possible_modes[1]:
                self.tool_class = self.preview_mode
            else:
                raise ValueError(f"Unknown mode: {current_mode}")
        except Exception as e:
            self.logger.Log(f"Error: {e}")

    def keyboard_controls(self):
        # switch mode using m key
        if px.btnp(px.KEY_M):
            if self.tool_mode == self.possible_modes[0]:
                self.tool_mode = self.possible_modes[1]
                self.mode_switcher(self.tool_mode)
            else:
                self.tool_mode = self.possible_modes[0]
                self.mode_switcher(self.tool_mode)

    def mouse_controls(self):
        self.mouse_pos = vec2(px.mouse_x, px.mouse_y)
        # center mouse on screen
        px.mouse_x = self.res_width // 2
        px.mouse_y = self.res_height // 2

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
        self.star_system.update()
        self.keyboard_controls()

    def render(self):
        px.cls(0)
        self.star_system.render()
        # print the current mode on the screen
        self.current_mode_render = self.tool_class.render()
        # render a box where the mouse is
        px.rectb(px.mouse_x - 8, px.mouse_y - 8, 4, 4, 7)

    def run(self):
        px.run(self.update, self.render)


if __name__ == "__main__":
    sb = SpawnBuilder()
    sb.run()
